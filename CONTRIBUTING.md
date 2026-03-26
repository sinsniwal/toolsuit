# Contributing to toolsuit

Thank you for your interest in contributing to toolsuit. This project aims to provide a robust, zero-dependency middleware for securing the boundary between LLM agents and Python backends.

We prioritize architectural cleanliness, strict type safety, and a zero-dependency footprint.

## Roadmap and Good First Issues

We are currently prioritizing the following features for the v0.2 release. If you would like to tackle one of these, please open an issue or comment on an existing one to coordinate efforts.

### 1. Async Support (async def)
The current implementation of @equip only handles synchronous functions. Given that many modern agentic frameworks (FastAPI, LangGraph) rely on asyncio, we need to extend the decorator to detect coroutines and await execution while preserving the signature modification.

### 2. Class Method Support (self/cls handling)
Wrapping methods within a class currently presents challenges with signature inspection. We need a reliable way to handle or bypass the 'self' or 'cls' parameters so they are not exposed to the LLM's tool schema.

### 3. Pydantic V2 Native Hooks
While signature rewriting works for basic tool calling, native integration with Pydantic V2's schema generation would offer deeper type validation and better compatibility with enterprise-grade validation engines.

---

## Development Setup

To contribute code, you will need Python 3.9 or higher.

1. **Clone the repository:**
```bash
git clone https://github.com/sinsniwal/toolsuit.git
```
cd toolsuit

3. **Install in editable mode with dev dependencies:**
```bash
pip install -e ".[dev]"
```

3. **Run the test suite:**
We use pytest for all unit testing. Ensure all tests pass before submitting a Pull Request.
```bash
pytest tests/
```

---

## Pull Request Process

To maintain the quality and security of the library, all contributions must adhere to the following guidelines:

* **Zero Dependencies:** PRs that introduce new production dependencies will be rejected. toolsuit must remain a lightweight, single-install utility.
* **Strict Typing:** All new functions and classes must include PEP 484 type hints.
* **Signature Integrity:** Any changes to the core execution loop must not break the `__signature__` modification logic that enables tool-calling compatibility.
* **Tests:** New features must include corresponding unit tests in the `tests/` directory.

We follow standard GitHub Flow. Create a feature branch from `main`, commit your changes, and open a Pull Request for review.
