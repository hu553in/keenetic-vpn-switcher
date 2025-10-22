# syntax=docker/dockerfile:1
FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT=/app/.venv

# Copy dependency manifests first for better caching
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy application source
COPY . .

# Run the bot via uv to ensure virtualenv isolation
CMD ["uv", "run", "python", "main.py"]
