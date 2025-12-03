"""
Pytest configuration and fixtures for agent-zero-hck tests.
"""

import sys
import os
import asyncio
import pytest

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_data_dir():
    """Return the path to test data directory."""
    return os.path.join(os.path.dirname(__file__), "data")


@pytest.fixture
def mock_config():
    """Provide a mock configuration for testing."""
    return {
        "model_provider": "openai",
        "model_name": "gpt-4.1-mini",
        "temperature": 0.7,
        "max_tokens": 2000,
    }


@pytest.fixture
def mock_settings():
    """Provide mock settings for testing."""
    return {
        "stt_model_size": "base",
        "embed_model_provider": "huggingface",
        "embed_model_name": "sentence-transformers/all-MiniLM-L6-v2",
        "tts_kokoro": False,
    }


def pytest_configure(config):
    """Configure pytest with custom settings."""
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers."""
    for item in items:
        # Add asyncio marker to async tests
        if asyncio.iscoroutinefunction(item.function):
            item.add_marker(pytest.mark.asyncio)
        
        # Add unit marker to tests in tests/ directory
        if "test_" in item.nodeid:
            item.add_marker(pytest.mark.unit)
