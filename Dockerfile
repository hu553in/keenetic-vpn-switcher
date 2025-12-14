# syntax=docker/dockerfile:1

FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS deps
WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT=/app/.venv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS runner
WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN useradd -m app

COPY --from=deps --chown=app:app /app/.venv ./.venv
COPY --chown=app:app pyproject.toml uv.lock main.py config.py ./

USER app
CMD ["uv", "run", "python", "main.py"]
