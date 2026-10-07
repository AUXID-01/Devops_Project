import io
import zipfile
import pytest

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["status"] == "healthy"
    assert res_data["database"] == "connected"
    assert "timestamp" in res_data

def create_project(client):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr("test.py", b"print('hello world')")
    
    files = {'file': ('test.zip', zip_buffer.getvalue(), 'application/zip')}
    data = {'name': 'Test Project'}
    
    response = client.post("/api/projects", data=data, files=files)
    return response.json()["id"]

def test_create_project(client):
    project_id = create_project(client)
    assert project_id > 0

def test_get_projects(client):
    create_project(client)
    
    response = client.get("/api/projects")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_create_and_get_bug(client):
    project_id = create_project(client)
    
    bug_data = {
        "title": "Test Bug",
        "description": "This is a test bug",
        "severity": "HIGH",
        "status": "OPEN",
        "affected_file": "main.py",
        "line_number": 10
    }
    
    response = client.post(f"/api/projects/{project_id}/bugs", json=bug_data)
    assert response.status_code == 200
    created_bug = response.json()
    assert created_bug["title"] == "Test Bug"
    bug_id = created_bug["id"]
    
    # Get the bug back
    response = client.get(f"/api/bugs/{bug_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Bug"

def test_update_bug(client):
    project_id = create_project(client)
    
    bug_data = {
        "title": "Update Test Bug",
        "description": "Testing update",
        "affected_file": "app.py"
    }
    
    response = client.post(f"/api/projects/{project_id}/bugs", json=bug_data)
    bug_id = response.json()["id"]
    
    update_data = {
        "status": "RESOLVED",
        "severity": "LOW"
    }
    
    response = client.put(f"/api/bugs/{bug_id}", json=update_data)
    assert response.status_code == 200
    updated_bug = response.json()
    assert updated_bug["status"] == "RESOLVED"
    assert updated_bug["severity"] == "LOW"

def test_delete_bug(client):
    project_id = create_project(client)
    
    bug_data = {
        "title": "Delete Me",
        "description": "To be deleted",
        "affected_file": "old.py"
    }
    
    response = client.post(f"/api/projects/{project_id}/bugs", json=bug_data)
    bug_id = response.json()["id"]
    
    response = client.delete(f"/api/bugs/{bug_id}")
    assert response.status_code == 200 # By default FastAPI returns 200 if not specified
    
    # Ensure it's deleted
    response = client.get(f"/api/bugs/{bug_id}")
    assert response.status_code == 404
