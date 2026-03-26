import inspect

import pytest
from toolsuit.core import equip


def test_signature_stripping():
    @equip(hide=["secret_key", "db_conn"])
    def my_tool(user_id: str, secret_key: str, db_conn: str = "mock"):
        return user_id

    sig = inspect.signature(my_tool)
    assert "user_id" in sig.parameters
    assert "secret_key" not in sig.parameters
    assert "db_conn" not in sig.parameters


def test_dependency_injection():
    # static
    @equip(hide=["api_key"], inject={"api_key": "sk_test_123"})
    def fetch_data(query: str, api_key: str):
        return f"{query}-{api_key}"

    assert fetch_data(query="hello") == "hello-sk_test_123"

    # dynamic
    @equip(inject={"token": lambda: "dyn_token"})
    def get_token(token: str):
        return token

    assert get_token() == "dyn_token"


def test_output_masking():
    def mask(result):
        return {"status": "ok", "count": len(result["data"])}

    @equip(mask_output=mask)
    def heavy_function():
        return {"data": [1, 2, 3, 4, 5], "secrets": "do_not_leak"}

    res = heavy_function()
    assert res == {"status": "ok", "count": 5}
    assert "secrets" not in res


def test_masking_error_suppression():
    def bad_mask(result):
        raise ValueError("Oops")

    @equip(mask_output=bad_mask)
    def heavy_function():
        return {"secrets": "super_secret_pki"}

    with pytest.raises(RuntimeError, match="Error occurred during output masking"):
        heavy_function()


def test_empty_equip():
    @equip()
    def simple_func(x: int):
        return x * 2

    assert simple_func(5) == 10
    assert "x" in inspect.signature(simple_func).parameters


def test_pydantic_compatibility():
    try:
        from typing import Any

        from pydantic import create_model
    except ImportError:
        pytest.skip("pydantic not installed")

    @equip(hide=["secret"])
    def my_func(user: str, secret: str = "123"):
        return user

    sig = inspect.signature(my_func)
    fields = {
        name: (
            param.annotation if param.annotation != inspect.Parameter.empty else Any,
            ...,
        )
        for name, param in sig.parameters.items()
    }
    # This should not raise an exception about missing definitions
    Model = create_model("MyFuncModel", **fields)
    assert "user" in Model.model_fields
    assert "secret" not in Model.model_fields


def test_positional_arg_binding():
    @equip(hide=["secret"], inject={"secret": "sssh"})
    def fetch_data(a, secret, b):
        return (a, secret, b)

    # The AI sees `fetch_data(a, b)`. If they call pos: `fetch_data(1, 2)`
    res = fetch_data(1, 2)
    assert res == (1, "sssh", 2)


def test_positional_only_args():
    # Demonstrating Python 3.8+ positional-only / keyword-only boundary works
    @equip(hide=["token"], inject={"token": "123"})
    def fetch_secure(a, /, token, *, c=None):
        return (a, token, c)

    res = fetch_secure("pos", c="kw")
    assert res == ("pos", "123", "kw")


def test_map_inputs_translation():
    def resolve_fake_id(faked: str) -> int:
        return {"user_A1": 1482, "user_B2": 9991}.get(faked, 0)

    @equip(map_inputs={"user_id": resolve_fake_id})
    def fetch_records(user_id: int, include_deleted: bool = False):
        return (user_id, include_deleted)

    # 1. AI passes the faked alias string it saw previously
    res_pos = fetch_records("user_A1")
    assert res_pos == (1482, False)

    # 2. Key-word invocation handled properly
    res_kw = fetch_records(user_id="user_B2", include_deleted=True)
    assert res_kw == (9991, True)
