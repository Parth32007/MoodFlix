"""
pytest configuration file for MoodFlix tests.
Defines fixtures, test discovery patterns, and pytest settings.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope='session')
def test_data_dir():
    """Get path to test data directory."""
    return Path(__file__).parent / 'data'


@pytest.fixture
def mock_config():
    """Fixture for mocking configuration."""
    config = {
        'TESTING': True,
        'DEBUG': False,
        'TMDB_API_KEY': 'test-key-12345',
        'RECOMMENDATION_COUNT': 5,
        'MOOD_WEIGHT': 0.7,
        'CONTENT_WEIGHT': 0.3,
    }
    return config


def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow"
    )


# Test discovery patterns
pytest_plugins = []
