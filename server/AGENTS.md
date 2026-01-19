# Repository Guidelines

## Project Structure & Module Organization
- Current repository content is minimal: `README.md` and this guide.
- Server code is expected to live under a source directory once added (for example, `src/` or `app/`).
- Tests should be placed in a dedicated directory such as `tests/` alongside fixtures or sample images.

## Build, Test, and Development Commands
- No build/test scripts are defined yet. When wiring them up, prefer a single entry point per task.
- Suggested pattern (once added):
  - `uv run python -m app` to start the FastAPI server.
  - `uv run pytest` to execute tests.

## Coding Style & Naming Conventions
- Python code should use 4-space indentation.
- Prefer `snake_case` for modules/functions and `PascalCase` for classes.
- Keep API routes and config keys lowercase and descriptive (for example, `/v1/parse`, `MODEL_PROVIDER`).
- If formatting tools are introduced, document them here (for example, `ruff format`).

## Testing Guidelines
- No test framework is currently configured. If tests are added, use `pytest` and name files `test_*.py`.
- Keep API-level tests close to request/response fixtures for fast iteration.

## Commit & Pull Request Guidelines
- Keep commit messages short and descriptive (existing history uses brief summaries like `project desc`).
- PRs should include: a concise summary, linked issue (if any), and test notes (command + result).

## Security & Configuration Tips
- Do not commit API keys or tokens. Store them in environment variables or a local `.env` file ignored by Git.
- When integrating LLM providers or memos APIs, document required env vars in `README.md`.
