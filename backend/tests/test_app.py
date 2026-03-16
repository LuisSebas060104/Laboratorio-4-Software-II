import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}

def test_student_cannot_create_task(client):
    nueva_tarea = {
        "course_code": "SW2",
        "title": "Tarea de Prueba",
        "description": "Validar prueba unitaria",
        "due_date": "2026-12-31"
    }
    response = client.post('/api/tasks', json=nueva_tarea, headers={"X-Role": "student"})
    
    assert response.status_code == 403
    assert "Solo un catedrático" in response.get_json()["error"]

def test_teacher_can_create_task(client):
    """Prueba funcional: Un profesor puede crear una tarea válida"""
    nueva_tarea = {
        "course_code": "SW2",
        "title": "Tarea del Profe",
        "description": "Descripcion de mas de diez caracteres",
        "due_date": "2026-12-30"
    }
    response = client.post('/api/tasks', json=nueva_tarea, headers={"X-Role": "teacher"})
    
    assert response.status_code == 201
    assert "id" in response.get_json()