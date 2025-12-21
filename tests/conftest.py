"""
Pytest configuration and fixtures for Agent-Zero-HCK tests.

This file ensures proper path setup for CI environments.
"""

import sys
import os
from pathlib import Path

# Ensure the project root is in the Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Set environment variables for testing
os.environ.setdefault("TESTING", "true")
os.environ.setdefault("LOG_LEVEL", "WARNING")


# Pytest fixtures
import pytest


@pytest.fixture
def project_root_path():
    """Return the project root path."""
    return project_root


@pytest.fixture
def test_data_dir(project_root_path):
    """Return the test data directory."""
    return project_root_path / "tests" / "data"


@pytest.fixture
def mock_agent_config():
    """Return a mock agent configuration for testing."""
    return {
        "name": "test-toga",
        "model": "gpt-4.1-mini",
        "personality": {
            "cheerfulness": 0.9,
            "playfulness": 0.85,
            "curiosity": 0.8,
        },
        "transform_quirk": {
            "enabled": True,
            "absorption_threshold": 0.7,
        },
        "security_testing": {
            "enabled": True,
            "ethical_constraints": True,
        },
    }


@pytest.fixture
def mock_personality():
    """Return a mock personality for testing."""
    from python.helpers.toga_personality import initialize_toga_personality

    return initialize_toga_personality()


@pytest.fixture
def mock_transform_quirk():
    """Return a mock transform quirk for testing."""
    from python.helpers.toga_transform import initialize_transform_quirk

    return initialize_transform_quirk()


@pytest.fixture
def mock_security_tester():
    """Return a mock security tester for testing."""
    from python.helpers.toga_security import initialize_toga_security_tester

    return initialize_toga_security_tester()
