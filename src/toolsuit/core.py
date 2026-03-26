import inspect
from functools import wraps
from typing import Any, Callable, Dict, List, Optional


def equip(
    hide: Optional[List[str]] = None,
    inject: Optional[Dict[str, Any]] = None,
    mask_output: Optional[Callable] = None,
    map_inputs: Optional[Dict[str, Callable]] = None,
):
    """
    Tailors a function for an AI agent by hiding arguments from the schema,
    injecting local state during execution, and masking heavy return data.

    Args:
        hide (Optional[List[str]]): List of argument names to remove from
            the function's signature. This prevents AI frameworks from
            trying to provide them.
        inject (Optional[Dict[str, Any]]): A dictionary of arguments to
            forcefully inject at runtime. Values can be static, or
            zero-argument callables for dynamic state.
        mask_output (Optional[Callable]): A filter function to sanitize or
            truncate the original function's raw return value before
            sending it back to the AI.
        map_inputs (Optional[Dict[str, Callable]]): A dictionary mapping
            AI-provided argument names to resolving functions. Used to
            translate faked IDs back to real internal IDs.

    Returns:
        Callable: The wrapped function with a modified `__signature__`.
    """
    hide_args = hide or []
    inject_args = inject or {}
    map_args = map_inputs or {}

    def decorator(func: Callable):
        sig = inspect.signature(func)

        # 1. Create a new signature dropping the hidden and injected args
        new_params = [
            param
            for name, param in sig.parameters.items()
            if name not in hide_args and name not in inject_args
        ]
        new_sig = sig.replace(parameters=new_params)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 1. Bind AI-provided arguments to our modified signature
            bound_ai = new_sig.bind(*args, **kwargs)
            bound_ai.apply_defaults()
            merged_kwargs = bound_ai.arguments.copy()

            # 2. Translation time: Resolve fake inputs to real primitives
            # (e.g., Aliases -> Database IDs)
            for key, resolver in map_args.items():
                if key in merged_kwargs:
                    merged_kwargs[key] = resolver(merged_kwargs[key])

            # 3. Execution time: Inject the secure/local variables
            for key, val_or_callable in inject_args.items():
                if callable(val_or_callable):
                    merged_kwargs[key] = val_or_callable()
                else:
                    merged_kwargs[key] = val_or_callable

            # 3. Carefully reconstruct args and kwargs for the original function
            final_args = []
            final_kwargs = {}
            for name, param in sig.parameters.items():
                if name in merged_kwargs:
                    if param.kind == inspect.Parameter.POSITIONAL_ONLY:
                        final_args.append(merged_kwargs[name])
                    elif param.kind in (
                        inspect.Parameter.POSITIONAL_OR_KEYWORD,
                        inspect.Parameter.KEYWORD_ONLY,
                    ):
                        final_kwargs[name] = merged_kwargs[name]
                    elif param.kind == inspect.Parameter.VAR_POSITIONAL:
                        final_args.extend(merged_kwargs[name])
                    elif param.kind == inspect.Parameter.VAR_KEYWORD:
                        final_kwargs.update(merged_kwargs[name])

            # 4. Run the original backend function dynamically
            raw_result = func(*final_args, **final_kwargs)

            # 4. Mask the output if a filter was provided
            if mask_output:
                try:
                    return mask_output(raw_result)
                except Exception:
                    # Raise a fresh exception without `from e` to ensure
                    # raw_result is not captured in the traceback frame.
                    raise RuntimeError(
                        "Error occurred during output masking. "
                        "Original exception suppressed to prevent data leakage."
                    )

            return raw_result

        # 5. Overwrite the signature so standard AI SDKs read the safe version
        wrapper.__signature__ = new_sig

        return wrapper

    return decorator
