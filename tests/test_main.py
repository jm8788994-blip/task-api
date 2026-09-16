from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_task():
    task = {
        "id": 1,
        "title": "Study FastAPI",
        "description": "Learn FastAPI basics",
        "status": "pending",
        "priority": "high"
    }

    response = client.post("/tasks", json=task)

    assert response.status_code == 200
    assert response.json()["title"] == "Study FastAPI"


def test_update_task():
    task = {
        "id": 1,
        "title": "Learn FastAPI",
        "description": "Updated description",
        "status": "completed",
        "priority": "high"
    }

    response = client.put("/tasks/1", json=task)

    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_delete_task():
    response = client.delete("/tasks/1")

    assert response.status_code == 200


# Invalid scenario 1
def test_get_nonexistent_task():
    response = client.delete("/tasks/999")

    assert response.status_code == 404


# Invalid scenario 2
def test_duplicate_task():
    task = {
        "id": 2,
        "title": "Task",
        "description": "Test task",
        "status": "pending",
        "priority": "low"
    }

    first_response = client.post("/tasks", json=task)
    second_response = client.post("/tasks", json=task)

    assert first_response.status_code == 200
    assert second_response.status_code == 400