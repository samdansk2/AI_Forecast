# Makefile for AI Progress Tracker
.PHONY: help install install-dev install-all sync update clean test lint format check run dashboard notebooks

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install project dependencies"
	@echo "  install-dev - Install with development dependencies"
	@echo "  install-all - Install all optional dependencies"
	@echo "  sync        - Sync dependencies from lock file"
	@echo "  update      - Update dependencies"
	@echo "  clean       - Remove virtual environment and cache"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linting tools"
	@echo "  format      - Format code"
	@echo "  check       - Run all checks (lint + test)"
	@echo "  run         - Run main application"
	@echo "  dashboard   - Start Streamlit dashboard"
	@echo "  notebooks   - Start Jupyter Lab"

# Installation commands
install:
	uv sync

install-dev:
	uv sync --extra dev

install-all:
	uv sync --all-extras

sync:
	uv sync --frozen

update:
	uv lock --upgrade
	uv sync

# Maintenance
clean:
	uv cache clean
	rm -rf .venv
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Development
test:
	uv run pytest

lint:
	uv run flake8 src/
	uv run mypy src/

format:
	uv run black .
	uv run isort .

check: format lint test

# Running applications
run:
	uv run ai-tracker

dashboard:
	uv run streamlit run dashboard/streamlit_app.py

notebooks:
	uv sync --extra notebook
	uv run jupyter lab

# Data operations
collect-data:
	uv run collect-data

analyze:
	uv run analyze-data

predict:
	uv run predict

visualize:
	uv run visualize
