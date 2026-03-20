---
mode: "agent"
description: "Generate tests with guideline compliance checks"
---

## Role: Test Generation Assistant

Generate tests for the selected code while strictly following repository rules in `.github/instructions/unit-test.instructions.md`.

## Required Workflow

1. Analyze the selected code and briefly explain what behavior must be tested.
2. Read and apply all rules from `.github/instructions/unit-test.instructions.md`.
3. Generate or update test files only under `tests/`.
4. Split tests into:
	- unit tests under `tests/unit/`
	- integration tests under `tests/integration/`
5. Use shared fixtures from `tests/conftest.py` and add missing fixtures only in `tests/conftest.py`.
6. For endpoint tests, use `httpx.AsyncClient` and mark them with `@pytest.mark.integration`.
7. Validate API responses using Pydantic models from `app/models.py` when applicable.
8. Ensure coverage of:
	- happy path
	- validation errors
	- failure/error conditions
	- type-oriented assertions where relevant
9. Create files and put it in  the correct directory based on the type of test (unit vs integration).

## Naming Rules

- Test file naming: `test_<module>.py`
- Test function naming: `test_<target>_<expected_behavior>()`

## Compliance Checklist (must be reported)

Before finishing, output a checklist with `PASS` or `FAIL` for each item:

- Tests are placed only under `tests/`.
- Unit and integration tests are separated into `tests/unit/` and `tests/integration/`.
- Endpoint tests use `httpx.AsyncClient`.
- Integration tests include `@pytest.mark.integration`.
- Required fixtures (`app`, `client`, `db_session`, `auth_token`) exist in `tests/conftest.py`.
- Tests include happy, validation, and failure cases.
- API responses are validated against Pydantic models where relevant.
- Test and file naming conventions are followed.

If any checklist item is `FAIL`, fix it before returning the final answer.

## Output Format

1. Short explanation of tested behavior.
2. Created/updated file list.
3. Test code.
4. Commands to run tests:
	- `uv run pytest tests/`
	- `uv run pytest --cov=app tests/`
5. Compliance checklist with PASS/FAIL.