"""Test config module."""
import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import config


def test_config_constants():
    """Test that config constants are properly defined."""
    assert hasattr(config, 'PROJECT_NAME')
    assert hasattr(config, 'VERSION')
    assert hasattr(config, 'AI_KEYWORDS')
    assert hasattr(config, 'DATA_PATHS')
    
    assert config.PROJECT_NAME == "AI Progress Tracker"
    assert config.VERSION == "1.0.0"
    assert isinstance(config.AI_KEYWORDS, list)
    assert len(config.AI_KEYWORDS) > 0


def test_ai_keywords():
    """Test AI keywords configuration."""
    assert 'artificial intelligence' in config.AI_KEYWORDS
    assert 'machine learning' in config.AI_KEYWORDS
    assert all(isinstance(keyword, str) for keyword in config.AI_KEYWORDS)


def test_data_paths():
    """Test data paths configuration."""
    assert 'milestones' in config.DATA_PATHS
    assert 'trends' in config.DATA_PATHS
    assert 'github' in config.DATA_PATHS
    assert 'processed' in config.DATA_PATHS
    
    # Check that paths are strings
    assert all(isinstance(path, str) for path in config.DATA_PATHS.values())
