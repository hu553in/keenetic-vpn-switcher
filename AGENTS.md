# Repository Guidelines

## Project Structure & Module Organization

The bot lives in `main.py`, orchestrating the Telegram handlers and Keenetic API calls.
Configuration parsing and validation sit in `config.py`, which all modules should reuse
for environment access. Docker artifacts (`Dockerfile`, `.dockerignore`) support container
builds, and `.github/workflows/docker.yml` publishes images on pushes to `main`.
Sample secrets stay in `.env.example`; keep real credentials in a private `.env`.
Add new Python modules alongside `main.py` or nest them under a new `keenetic_switcher/`
package when the codebase grows; mirror tests under `tests/`.

## Build, Test, and Development Commands

- `uv sync` — install pinned dependencies from `pyproject.toml` / `uv.lock`.
- `uv run --env-file .env python main.py` — run the bot locally with your device list and router secrets.
- `docker build -t keenetic-vpn-switcher .` — produce a container image identical to CI.
- `docker run --env-file .env keenetic-vpn-switcher` — verify the image end to end.

## Coding Style & Naming Conventions

Target Python 3.13 with PEP 8 formatting and 4-space indentation. Prefer dataclasses or plain dicts
for new config payloads, and keep device-related helpers pure for easier testing. Name async callbacks
`handle_*` and synchronous helpers `apply_*` or `build_*`, matching existing patterns. Use `LOGGER`
for structured messages and lowercase environment keys that mirror Keenetic terminology.

## Testing Guidelines

Adopt `pytest` for new coverage. Place cases in `tests/` and mirror module names
(e.g., `tests/test_config.py`). Exercise config validation using fixture `.env` samples
and mock `requests.Session` for policy flows. Run `uv run pytest` locally and ensure
CI-ready tests avoid hitting real routers; use responses or HTTP mocks instead.

## Commit & Pull Request Guidelines

Follow Conventional Commits (`feat:`, `fix:`, `chore:`) as seen in history. Keep commits focused and
include configuration or schema updates alongside their code. Pull requests should describe behavior
changes, list manual verification steps (`uv run --env-file .env python main.py`), and reference
supporting issues. Include screenshots or logs when tweaking bot replies or inline keyboards.

## Security & Configuration Tips

Never commit `.env`; rely on `.env.example` for placeholders. Rotate router passwords and bot tokens
when rotating maintainers. Scrub logs before sharing because callbacks may include user identifiers.
For self-hosted deployments, prefer GitHub environment secrets and pass them into the container runtime.
