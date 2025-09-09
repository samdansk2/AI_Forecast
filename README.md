# AI Forecast

A comprehensive machine learning system that analyzes global AI market trends, predicts future growth patterns, and provides actionable insights for investors and businesses in the artificial intelligence sector.

## 📋 Overview

This project leverages advanced data science techniques to process and analyze AI market data from multiple sources, providing detailed insights.

##  Key Features

- 📊 **Data Processing Pipeline** - Automated data cleaning and feature engineering
- 🤖 **Machine Learning Models** - Multiple ML algorithms (Linear Regression, Random Forest, XGBoost, etc.)
- 📈 **Interactive Dashboard** - Streamlit-based web application with real-time analytics
- 🌍 **Geographic Analysis** - Country and city-level AI popularity insights
- ⚡ **Performance Optimized** - Efficient data processing with modern Python tools

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- [UV](https://docs.astral.sh/uv/) package manager (recommended) or pip

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/samdansk2/ML_project.git
cd ML_project
```

1. **Create environment**:

```bash
uv init
uv venv
uv pip install -r requirements.txt
```

### Running the Application

**Start the Interactive Dashboard:**
```bash
# Using UV
uv run streamlit run dashboard/enhanced_app.py

# Using pip
streamlit run dashboard/enhanced_app.py
```

## 🤖 Machine Learning Models

The system implements multiple ML algorithms for robust predictions:

- **Linear Regression** - Baseline trend analysis
- **Ridge & Lasso Regression** - Regularized linear models
- **Random Forest** - Ensemble learning for complex patterns
- **Gradient Boosting** - Advanced boosting algorithm
- **XGBoost** - Optimized gradient boosting

## 🔧 Development

### Setting up Development Environment

```bash
# Install with development dependencies
uv sync --extra dev

# Run tests
uv run pytest

# Code formatting
uv run black .
uv run isort .

# Type checking
uv run mypy .
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`uv sync --extra dev`)
4. Open a Pull Request

## 🙋‍♂️ Support

If you encounter any issues or have questions:

- Open an [issue](https://github.com/samdansk2/ML_project/issues) on GitHub
- Review the [notebooks](notebooks/) for implementation examples