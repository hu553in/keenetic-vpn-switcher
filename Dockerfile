# syntax=docker/dockerfile:1

FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS deps
WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT=/app/.venv \
  UV_CACHE_DIR=/root/.cache/uv

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --locked --no-dev

FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS runner
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  UV_PROJECT_ENVIRONMENT=/app/.venv \
  UV_CACHE_DIR=/tmp/uv-cache

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
  apt-get update && \
  apt-get upgrade -y --no-install-recommends

# Runtime dependencies come from the built virtualenv; pip is unused.
RUN python -m pip uninstall --yes pip \
  && useradd -m app

COPY --from=deps --chown=app:app /app/.venv ./.venv
COPY --chown=app:app pyproject.toml uv.lock main.py config.py ./

USER app
CMD ["/app/.venv/bin/python", "main.py"]
