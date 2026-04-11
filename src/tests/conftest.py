from src.db.main import get_session
from src import main
from unittest.mock import Mock
from fastapi.testclient import TestClient
import pytest
mock_session = Mock()
mock_user_service = Mock()

def get_mock_session():
    return mock_session

app.dependency_overrides[get_session]= get_mock_session

@pytest.fixture
def fake_session():
    return mock_session

@pytest.fixture
def fake_user_service():
    return mock_user_service

@pytest.fixture
def test_client():
    return TestClient(main.app)