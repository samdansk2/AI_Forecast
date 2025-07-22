# UV Best Practices Guide

This document outlines the UV best practices implemented in this AI Progress Tracker project.

## 🚀 Quick Start

### Windows
```powershell
# Run the setup script
.\setup.bat

# Or manually
uv sync --all-extras
```

### macOS/Linux
```bash
# Run the setup script
python setup.py

# Or manually
uv sync --all-extras
```

## 📋 UV Best Practices Implemented

### 1. Project Configuration (`pyproject.toml`)

✅ **Complete metadata**: Project name, description, authors, license
✅ **Python version constraints**: `requires-python = ">=3.9"`
✅ **Dependency management**: Clear main and optional dependencies
✅ **Script definitions**: CLI commands for easy execution
✅ **Tool configurations**: Black, isort, mypy, pytest settings

### 2. Dependency Management

✅ **Optional dependencies**: Organized into logical groups
- `dev`: Development tools (pytest, black, isort, mypy)
- `notebook`: Jupyter and related packages
- `docs`: Documentation tools

✅ **Version pinning**: Appropriate version constraints
```toml
dependencies = [
    "pandas>=1.5.0",
    "numpy>=1.21.0,<2.0.0",
]
```

### 3. Virtual Environment Management

✅ **Automatic venv creation**: UV creates `.venv` automatically
✅ **Python version control**: `.python-version` file specifies Python 3.11
✅ **Isolation**: All dependencies isolated in project venv

### 4. Lock File Management

✅ **Reproducible builds**: `uv.lock` ensures consistent installs
✅ **Version control**: Lock file tracked in Git
✅ **Updates**: Easy dependency updates with `uv lock --upgrade`

### 5. Script Commands

Defined in `pyproject.toml`:
```toml
[project.scripts]
ai-tracker = "src.main:main"
collect-data = "src.data_collector:main"
analyze-data = "src.analyzer:main"
predict = "src.predictor:main"
visualize = "src.visualizations:main"
```

Usage:
```bash
uv run ai-tracker          # Run main application
uv run collect-data        # Collect AI data
uv run analyze-data        # Analyze data
uv run predict             # Generate predictions
uv run visualize           # Create visualizations
```

### 6. Development Workflow

✅ **Code formatting**: Black and isort configured
✅ **Type checking**: MyPy with strict settings
✅ **Linting**: Flake8 for code quality
✅ **Testing**: Pytest with coverage reporting
✅ **Pre-commit hooks**: Automated code quality checks

Commands:
```bash
# Install dev dependencies
uv sync --extra dev

# Format code
uv run black .
uv run isort .

# Type check
uv run mypy src/

# Run tests
uv run pytest

# Install pre-commit hooks
uv run pre-commit install
```

### 7. Makefile Integration

Common tasks simplified:
```bash
make install        # Install dependencies
make install-dev    # Install with dev dependencies
make test          # Run tests
make format        # Format code
make lint          # Run linting
make clean         # Clean up artifacts
```

### 8. Docker-Ready Configuration

Project structure supports containerization:
- All dependencies in `pyproject.toml`
- UV can be used in Docker for fast, reproducible builds
- Lock file ensures consistency across environments

### 9. IDE Integration

✅ **VS Code settings**: Tool configurations work with VS Code
✅ **PyCharm compatibility**: Standard Python project structure
✅ **Type hints**: Full type annotation support

### 10. CI/CD Ready

The project structure supports:
- GitHub Actions workflows
- Docker builds
- Automated testing and deployment
- Dependency security scanning

## 🔧 UV Commands Reference

### Installation
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh  # Unix
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows
```

### Project Setup
```bash
# Install all dependencies
uv sync

# Install with specific extras
uv sync --extra dev
uv sync --extra notebook
uv sync --all-extras

# Install from lock file (production)
uv sync --frozen
```

### Dependency Management
```bash
# Add dependency
uv add pandas

# Add dev dependency
uv add --dev pytest

# Add optional dependency
uv add --optional notebook jupyter

# Remove dependency
uv remove package-name

# Update dependencies
uv lock --upgrade
```

### Running Commands
```bash
# Run Python
uv run python

# Run scripts
uv run python -m module
uv run script-name

# Run with specific Python version
uv run --python 3.11 python script.py
```

### Environment Management
```bash
# Show environment info
uv run python --version

# Show installed packages
uv pip list

# Install package in current env
uv pip install package-name
```

## 📁 Project Structure

```
ML_project/
├── .python-version          # Python version specification
├── pyproject.toml           # Project configuration and dependencies
├── uv.lock                  # Dependency lock file (generated)
├── .gitignore              # Git ignore rules (UV-optimized)
├── .pre-commit-config.yaml # Pre-commit hooks configuration
├── Makefile                # Common task automation
├── setup.py                # Cross-platform setup script
├── setup.bat               # Windows setup script
├── README.md               # Project documentation
├── src/                    # Source code
├── tests/                  # Test files
├── data/                   # Data directories
├── results/                # Output directories
├── dashboard/              # Streamlit dashboard
├── notebooks/              # Jupyter notebooks
└── docs/                   # Documentation
```

## 🎯 Benefits Achieved

1. **Fast installations**: UV's Rust-based resolver is significantly faster than pip
2. **Reproducible environments**: Lock files ensure consistent installations
3. **Clear dependency management**: Organized optional dependencies
4. **Developer experience**: Integrated tooling and scripts
5. **Type safety**: Full type checking with MyPy
6. **Code quality**: Automated formatting and linting
7. **Easy CI/CD**: Standard structure supports automation
8. **Cross-platform**: Works on Windows, macOS, and Linux

## 🔍 Troubleshooting

### Common Issues

1. **UV not found**
   ```bash
   # Reinstall UV
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Python version mismatch**
   ```bash
   # Install specific Python version
   uv python install 3.11
   ```

3. **Lock file conflicts**
   ```bash
   # Regenerate lock file
   rm uv.lock
   uv lock
   ```

4. **Cache issues**
   ```bash
   # Clear UV cache
   uv cache clean
   ```

## 📚 Additional Resources

- [UV Documentation](https://docs.astral.sh/uv/)
- [Python Packaging Guide](https://packaging.python.org/)
- [PEP 621 - Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [UV GitHub Repository](https://github.com/astral-sh/uv)
