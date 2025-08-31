# AI Progress Tracker

A comprehensive tool for analyzing and visualizing AI development milestones and trends using data collection, analysis, and machine learning techniques.

## Features

- 📊 **Data Collection**: Gather AI milestone data and Google Trends
- 🔍 **Analysis**: Analyze AI development patterns and trends
- 🤖 **Predictions**: Machine learning models for trend forecasting
- 📈 **Visualization**: Interactive charts and dashboards
- 🌐 **Web Dashboard**: Streamlit-based interactive interface

## Prerequisites

- Python 3.9 or higher
- [UV](https://docs.astral.sh/uv/) package manager

## Installation

### Install UV (if not already installed)

On Windows (PowerShell):
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

On macOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Project Setup

1. **Clone the repository**:
```bash
git clone https://github.com/samdansk2/ML_project.git
cd ML_project
```

2. **Install dependencies using UV**:
```bash
# Install all dependencies
uv sync

# Install with development dependencies
uv sync --extra dev

# Install with notebook dependencies
uv sync --extra notebook

# Install all optional dependencies
uv sync --all-extras
```

3. **Activate the virtual environment**:
```bash
# On Windows
uv run python --version

# Or activate manually
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

## Usage

### Running the Application

```bash
# Run the main analysis
uv run ai-tracker

# Collect data
uv run collect-data

# Analyze existing data
uv run analyze-data

# Generate predictions
uv run predict

# Create visualizations
uv run visualize

# Start the Streamlit dashboard
uv run streamlit run dashboard/streamlit_app.py
```

### Development Workflow

```bash
# Install development dependencies
uv sync --extra dev

# Run tests
uv run pytest

# Format code
uv run black .
uv run isort .

# Lint code
uv run flake8 src/
uv run mypy src/

# Install pre-commit hooks
uv run pre-commit install
```

### Working with Notebooks

```bash
# Install notebook dependencies
uv sync --extra notebook

# Start Jupyter Lab
uv run jupyter lab

# Start Jupyter Notebook
uv run jupyter notebook
```

### Managing Dependencies

```bash
# Add a new dependency
uv add pandas

# Add a development dependency
uv add --dev pytest

# Add an optional dependency
uv add --optional notebook jupyterlab

# Remove a dependency
uv remove package-name

# Update all dependencies
uv lock --upgrade

# Install from lock file
uv sync --frozen
```

## Project Structure

```
ML_project/
├── data/                   # Data directory
│   ├── raw/               # Raw data files
│   └── processed/         # Processed data files
├── notebooks/             # Jupyter notebooks
├── results/               # Output results
├── docs/                  # Documentation
├── pyproject.toml         # Project configuration
├── uv.lock               # Dependency lock file
└── .python-version       # Python version specification
```

## Configuration

Edit `config.py` to customize:
- Data collection parameters
- AI keywords for trend analysis
- File paths and visualization settings

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Install development dependencies: `uv sync --extra dev`
4. Make your changes and add tests
5. Run the test suite: `uv run pytest`
6. Format code: `uv run black . && uv run isort .`
7. Commit your changes: `git commit -am 'Add feature'`
8. Push to the branch: `git push origin feature-name`
9. Submit a pull request

## UV Best Practices Used

This project follows UV best practices:

- ✅ **pyproject.toml configuration**: Complete project metadata and dependencies
- ✅ **Lock file management**: Reproducible builds with `uv.lock`
- ✅ **Optional dependencies**: Organized extras for different use cases
- ✅ **Script definitions**: CLI commands defined in pyproject.toml
- ✅ **Python version pinning**: `.python-version` file for consistency
- ✅ **Development workflow**: Integrated linting, formatting, and testing
- ✅ **Virtual environment**: Automatic venv management
- ✅ **Fast installs**: Parallel dependency resolution and caching

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please [open an issue](https://github.com/samdansk2/ML_project/issues) on GitHub.