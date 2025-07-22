"""Test configuration and fixtures."""
import pytest
import sys
from pathlib import Path

# Add src to Python path for testing
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def sample_data():
    """Provide sample data for testing."""
    return {
        "ai_keywords": ["artificial intelligence", "machine learning"],
        "dates": ["2020-01-01", "2021-01-01", "2022-01-01"],
        "values": [10, 20, 30]
    }


@pytest.fixture
def config_data():
    """Provide configuration data for testing."""
    return {
        "PROJECT_NAME": "AI Progress Tracker",
        "VERSION": "1.0.0",
        "AI_KEYWORDS": ["artificial intelligence", "machine learning"]
    }
