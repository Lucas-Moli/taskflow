import json

import pytest

from src.models.task import Task


@pytest.fixture(autouse=True)
def api_seed(seed_tasks):
    seed_tasks(
        [
            Task(1, "Tarefa A", "Descrição A", "Alta", "Pendente"),
            Task(2, "Tarefa B", "Descrição B", "Média", "Em andamento"),
        ],
        next_id=3,
    )


@pytest.mark.integration
def test_api_list_tasks(client):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2


@pytest.mark.integration
def test_api_get_task(client):
    response = client.get("/api/tasks/1")
    assert response.status_code == 200
    assert json.loads(response.data)["title"] == "Tarefa A"


@pytest.mark.integration
def test_api_get_task_not_found(client):
    assert client.get("/api/tasks/999").status_code == 404


@pytest.mark.integration
def test_api_search_and_filter(client):
    response = client.get("/api/tasks?search=tarefa%20b&priority=Média&status=Em andamento")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]["title"] == "Tarefa B"


@pytest.mark.integration
def test_api_create_task(client):
    response = client.post(
        "/api/tasks",
        json={
            "title": "Nova via API",
            "description": "Criada pelo REST",
            "priority": "Baixa",
        },
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["title"] == "Nova via API"
    assert data["status"] == "Pendente"


@pytest.mark.integration
def test_api_create_invalid_priority(client):
    response = client.post(
        "/api/tasks",
        json={"title": "X", "description": "Y", "priority": "Urgente"},
    )
    assert response.status_code == 400
    assert "error" in json.loads(response.data)


@pytest.mark.integration
def test_api_update_and_complete(client):
    update = client.put(
        "/api/tasks/1",
        json={
            "title": "Atualizada",
            "description": "Nova desc",
            "priority": "Baixa",
            "status": "Em andamento",
        },
    )
    assert update.status_code == 200
    assert json.loads(update.data)["title"] == "Atualizada"

    complete = client.post("/api/tasks/1/complete")
    assert complete.status_code == 200
    assert json.loads(complete.data)["status"] == "Concluída"


@pytest.mark.integration
def test_api_delete_task(client):
    response = client.delete("/api/tasks/2")
    assert response.status_code == 204
    assert client.get("/api/tasks/2").status_code == 404


@pytest.mark.integration
def test_api_metadata(client):
    response = client.get("/api/tasks/metadata")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "Alta" in data["priorities"]
    assert "Concluída" in data["statuses"]


@pytest.mark.integration
def test_api_update_not_found(client):
    response = client.put(
        "/api/tasks/999",
        json={"title": "X", "description": "Y", "priority": "Alta", "status": "Pendente"},
    )
    assert response.status_code == 404
