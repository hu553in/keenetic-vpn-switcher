SHELL := /bin/bash
.ONESHELL:
.SHELLFLAGS := -euo pipefail -c

.PHONY: install-deps
install-deps:
	uv sync --frozen --no-install-project

.PHONY: sync-deps
sync-deps:
	uv sync

.PHONY: check-deps-updates
check-deps-updates:
	uv tree --outdated --depth=1 | grep latest

.PHONY: check-deps-vuln
check-deps-vuln:
	uv run pysentry-rs .

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
