"""Minimal pytest config."""

import pytest

pytest_plugins = []  # Add plugins if needed

@pytest.fixture(scope="session")
def test_client():
    """Provide test client for API tests."""
    from fastapi.testclient import TestClient
    from api.main import app
    return TestClient(app)
