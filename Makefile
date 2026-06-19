SHELL := /bin/bash
.ONESHELL:
.SHELLFLAGS := -euo pipefail -c

.PHONY: install-deps
install-deps:
	uv sync --frozen --no-install-project

.PHONY: lint
lint:
	uv run ruff format
	uv run ruff check --fix

.PHONY: check-types
check-types:
	uv run ty check .

.PHONY: check
check:
	uv run prek --all-files --hook-stage pre-commit
