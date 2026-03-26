# toolsuit

[![PyPI](https://badge.fury.io/py/toolsuit.svg)](https://pypi.org/project/toolsuit/)
[![Tests](https://github.com/sinsniwal/toolsuit/actions/workflows/test.yml/badge.svg)](https://github.com/sinsniwal/toolsuit/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Stop giving LLMs direct access to your raw backend.**

`toolsuit` is a zero-dependency Python decorator that acts as a secure middleware between your AI agents (LangChain, OpenAI, Anthropic, Pydantic) and your actual code.

If you pass backend functions directly to AI SDKs, the LLM reads your entire signature. It will try to hallucinate database connection strings, expose secure API keys, and blow up your token limits by reading massive return payloads it doesn't need.

`toolsuit` dynamically rewrites the `__signature__` of your function at import-time. It tailors the function so the AI only sees a clean, lightweight schema, while your backend safely handles the heavy lifting locally.

### Installation

```bash
pip install toolsuit
```

### Why use Toolsuit?

- **Zero-Knowledge Security:** The AI never sees your API keys, database sessions, or local environment variables.
- **Token Efficiency:** Stop feeding 10MB database rows back into the context window just to tell the AI an operation succeeded.
- **Prevents Hallucinations:** A clean, minimal function signature keeps the agent focused and prevents it from hallucinating system-level arguments.

---

### Quickstart: The `@equip` Decorator

You don't need to rewrite your backend logic. Just decorate it. `toolsuit` intercepts the execution loop, natively tricking standard SDKs (like Pydantic or OpenAI) into generating a safe schema.

```python
from typing import Any, Dict
from toolsuit import equip

@equip(
hide=["db_session"],# 1. HIDE: Completely remove these from the AI's generated JSON schema
inject={"db_session": lambda: get_secure_database()}, # 2. INJECT: Securely fetch the missing state locally at runtime
alias={"user_id": lambda ai_string: resolve_internal_uuid(ai_string)}, # 3. ALIAS: Translate the AI's simplified input into your complex local internal ID
mask_output=lambda raw_row: {"status": "ok", "user": raw_row.get("public_alias")} # 4. MASK: Strip the massive raw output down to exactly what the AI needs

)
def fetch_user(user_id: str, db_session: Any) -> Dict[str, Any]:
"""Fetches a user profile from the secure database.""" # Your unmodified backend logic runs here securely
return {
"public_alias": "usr_fake",
"internal_id": user_id,
"password": "super_secret_hash_992",
"credit_card": "4242_1111_2222_3333"
}
```

### Execution Trace

When you pass `fetch_user` to your AI agent, `toolsuit` cleanly intercepts the translation layer.

> **1. What the AI Schema Parser sees:**
> A perfectly clean, safe function. No database sessions, no secrets.
> ```python
> def fetch_user(user_id: str):
> """Fetches a user profile from the secure database."""
> ```

> **2. What the AI sends during execution:**
> ```json
> {
> "name": "fetch_user",
> "arguments": {"user_id": "usr_fake"}
> }
> ```

> **3. What the AI receives after execution:**
> The massive database row full of PII and passwords was masked securely on your server. The AI only gets the lightweight summary.
> ```json
> {
> "status": "ok",
> "user": "usr_fake"
> }
> ```

---

### Limitations & Roadmap

- **Status: Sync Only.** Currently supports synchronous functions only. Async support (`async def`) is coming in `v0.2`.
- **Methods:** Class method support (`self` parameter handling) is under active development.

### Contributing

Toolsuit is actively looking for open-source contributors. See [CONTRIBUTING.md](CONTRIBUTING.md) for current issues, architecture details, and good first issues.
