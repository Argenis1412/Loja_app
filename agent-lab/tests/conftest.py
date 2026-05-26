import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_gemini(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("agents.scout.call_gemini", mock)
    return mock

@pytest.fixture
def mock_claude(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("agents.architect.call_claude", mock)
    return mock

@pytest.fixture
def mock_groq(monkeypatch):
    mock = MagicMock()
    # Mocking individual methods instead of entire module where possible
    monkeypatch.setattr("agents.executor._call_groq", mock)
    return mock

@pytest.fixture
def mock_subprocess(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("subprocess.run", mock)
    return mock
