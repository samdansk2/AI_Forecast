# 🚀 AI Market Intelligence System

A comprehensive machine learning system that analyzes global AI market trends, predicts future growth patterns, and provides actionable insights for investors and businesses in the artificial intelligence sector.

## 📋 Overview

This project leverages advanced data science techniques to process and analyze AI market data from multiple sources, providing detailed insights into:

- **Global AI Market Value Trends** - Historical and projected market valuations
- **AI Software Revenue Growth** - Revenue patterns across different AI sectors  
- **Regional AI Adoption Patterns** - Geographic distribution of AI interest and implementation
- **Predictive Market Modeling** - Machine learning models for forecasting future trends
- **Interactive Visualizations** - Professional dashboards for data exploration

## ✨ Key Features

- 📊 **Data Processing Pipeline** - Automated data cleaning and feature engineering
- 🤖 **Machine Learning Models** - Multiple ML algorithms (Linear Regression, Random Forest, XGBoost, etc.)
- 📈 **Interactive Dashboard** - Streamlit-based web application with real-time analytics
- 🌍 **Geographic Analysis** - Country and city-level AI popularity insights
- 📝 **Comprehensive Reports** - Automated generation of market analysis reports
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

2. **Install dependencies**:

Using UV (recommended):
```bash
# Install all dependencies
uv sync

# Or install with specific extras
uv sync --extra dev --extra notebook
```

Using pip:
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

**Start the Interactive Dashboard:**
```bash
# Using UV
uv run streamlit run dashboard/enhanced_app.py

# Using pip
streamlit run dashboard/enhanced_app.py
```

**Run Analysis Scripts:**
```bash
# Process data and generate insights
uv run python notebooks/02_data_cleaning.ipynb  # Data cleaning
uv run python notebooks/05_model_development.ipynb  # ML modeling
```

## 📁 Project Structure

```
ML_project/
├── dashboard/             # Interactive Streamlit dashboard
│   └── enhanced_app.py   # Main dashboard application
├── data/                 # Data storage
│   ├── raw/             # Original datasets
│   │   ├── AI_ML_popularity.csv
│   │   └── The_Rise_of_AI.csv
│   └── processed/       # Cleaned and processed data
├── notebooks/           # Jupyter notebooks for analysis
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_eda_visualization.ipynb
│   ├── 05_model_development.ipynb
│   └── 06_predictions.ipynb
├── models/              # Trained ML models
│   ├── aisoftwarerevenueinbillions/
│   └── globalaimarketvalueinbillions/
├── results/             # Analysis outputs and visualizations
└── docs/               # Documentation
```

## 🔬 Analysis Workflow

1. **Data Exploration** (`01_data_exploration.ipynb`) - Initial data investigation
2. **Data Cleaning** (`02_data_cleaning.ipynb`) - Data preprocessing and quality checks
3. **Feature Engineering** (`03_feature_engineering.ipynb`) - Creating predictive features
4. **EDA & Visualization** (`04_eda_visualization.ipynb`) - Exploratory data analysis
5. **Model Development** (`05_model_development.ipynb`) - Training ML models
6. **Predictions** (`06_predictions.ipynb`) - Generating forecasts and insights

## 🎯 Use Cases

- **Investment Analysis** - Identify emerging AI market opportunities
- **Strategic Planning** - Understand regional AI adoption patterns
- **Market Research** - Analyze competitive landscapes and growth trends
- **Risk Assessment** - Evaluate market volatility and investment risks
- **Business Intelligence** - Generate data-driven insights for decision making

## 🛠️ Technologies Used

- **Python 3.9+** - Core programming language
- **Pandas & NumPy** - Data manipulation and analysis
- **Scikit-learn** - Machine learning algorithms
- **XGBoost** - Gradient boosting framework
- **Streamlit** - Interactive web dashboard
- **Plotly** - Advanced data visualizations
- **Matplotlib & Seaborn** - Statistical plotting
- **UV** - Modern Python package management

## 📊 Dataset

The project analyzes two main datasets:

1. **AI Market Growth Data** (`The_Rise_of_AI.csv`)
   - AI software revenue trends (2018-2025)
   - Global AI market valuations
   - AI adoption rates and organizational metrics
   - Job market impact analysis

2. **Global AI Popularity Data** (`AI_ML_popularity.csv`)
   - Country and city-level AI interest metrics
   - Search trends for AI-related topics
   - Geographic distribution of AI adoption

## 🤖 Machine Learning Models

The system implements multiple ML algorithms for robust predictions:

- **Linear Regression** - Baseline trend analysis
- **Ridge & Lasso Regression** - Regularized linear models
- **Random Forest** - Ensemble learning for complex patterns
- **Gradient Boosting** - Advanced boosting algorithm
- **XGBoost** - Optimized gradient boosting

## 📈 Dashboard Features

The interactive Streamlit dashboard provides:

- **Real-time Market Analytics** - Live charts and metrics
- **Predictive Forecasting** - ML-powered market predictions
- **Geographic Insights** - Regional AI adoption heatmaps
- **Model Comparison** - Performance metrics across different algorithms
- **Export Capabilities** - Download insights and visualizations

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

### Running Jupyter Notebooks

```bash
# Install notebook dependencies
uv sync --extra notebook

# Start Jupyter Lab
uv run jupyter lab
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`uv sync --extra dev`)
4. Make your changes and add tests
5. Run the test suite (`uv run pytest`)
6. Format your code (`uv run black . && uv run isort .`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

If you encounter any issues or have questions:

- Open an [issue](https://github.com/samdansk2/ML_project/issues) on GitHub
- Check the [documentation](docs/) for detailed guides
- Review the [notebooks](notebooks/) for implementation examples

## 🌟 Acknowledgments

- Data sources for AI market trends and popularity metrics
- Open-source machine learning community
- Streamlit framework for interactive dashboards

---

Made with ❤️ for the AI research community