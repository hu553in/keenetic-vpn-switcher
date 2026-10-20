# syntax=docker/dockerfile:1

FROM python:3.15-slim-trixie AS deps
COPY --from=ghcr.io/astral-sh/uv:0.13.2 /uv /uvx /bin/
WORKDIR /app

ENV UV_CACHE_DIR=/root/.cache/uv \
  UV_PROJECT_ENVIRONMENT=/app/.venv \
  UV_PYTHON_DOWNLOADS=0

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --locked --no-dev

FROM python:3.15-slim-trixie AS runner
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
  apt-get update \
  && apt-get upgrade -y --no-install-recommends

# Runtime dependencies come from the built virtualenv; pip is unused.
RUN python -m pip uninstall --yes pip \
  && useradd -m app

COPY --from=deps --chown=app:app /app/.venv ./.venv
COPY --chown=app:app pyproject.toml uv.lock main.py config.py ./

USER app
CMD ["/app/.venv/bin/python", "main.py"]
