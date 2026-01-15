"""Test suite for the todo backend API."""
import pytest
from fastapi.testclient import TestClient
from main import app
from models import TaskCreate, TaskUpdate


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_task_missing_auth(client):
    """Test creating a task without authentication (should fail)."""
    task_data = {"title": "Test task", "description": "Test description"}
    response = client.post("/api/v1/tasks", json=task_data)
    assert response.status_code == 401  # Unauthorized


def test_get_tasks_missing_auth(client):
    """Test getting tasks without authentication (should fail)."""
    response = client.get("/api/v1/tasks")
    assert response.status_code == 401  # Unauthorized


def test_get_specific_task_missing_auth(client):
    """Test getting a specific task without authentication (should fail)."""
    response = client.get("/api/v1/tasks/1")
    assert response.status_code == 401  # Unauthorized


def test_update_task_missing_auth(client):
    """Test updating a task without authentication (should fail)."""
    task_update = {"title": "Updated title"}
    response = client.put("/api/v1/tasks/1", json=task_update)
    assert response.status_code == 401  # Unauthorized


def test_toggle_completion_missing_auth(client):
    """Test toggling task completion without authentication (should fail)."""
    response = client.patch("/api/v1/tasks/1/complete")
    assert response.status_code == 401  # Unauthorized


def test_delete_task_missing_auth(client):
    """Test deleting a task without authentication (should fail)."""
    response = client.delete("/api/v1/tasks/1")
    assert response.status_code == 401  # Unauthorized