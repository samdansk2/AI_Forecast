from datetime import datetime

# Project settings
PROJECT_NAME = "AI Progress Tracker"
VERSION = "1.0.0"

# Data file paths
DATA_PATHS = {
    'milestones': 'data/milestones.csv',
    'trends': 'data/raw/google_trends.csv',
    'github': 'data/raw/github_activity.csv',
    'processed': 'data/processed/combined_data.csv'
}

# Visualization settings
PLOT_STYLE = 'seaborn-v0_8'
FIGURE_SIZE = (12, 8)
COLOR_PALETTE = 'husl'

# Prediction settings
PREDICTION_HORIZON_YEARS = 5
CONFIDENCE_LEVEL = 0.95