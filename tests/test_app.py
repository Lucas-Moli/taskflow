import pytest

from src.models.task import Task
from src.repositories.task_repository import TASKS_DB


@pytest.mark.integration
def test_index_returns_ok(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"TaskFlow" in response.data
    assert b"Painel operacional" in response.data


@pytest.mark.integration
def test_create_task(client):
    response = client.post(
        "/task/create",
        data={
            "title": "Despachar carga perecível",
            "description": "Container refrigerado do porto de Santos.",
            "priority": "Alta",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Despachar carga perec\xc3\xadvel" in response.data
    assert any(t.title == "Despachar carga perecível" for t in TASKS_DB)


@pytest.mark.integration
def test_update_task(client):
    response = client.post(
        "/task/update/1",
        data={
            "title": "Frotas atualizadas",
            "description": "Nova descrição",
            "priority": "Média",
            "status": "Em andamento",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    task = next(t for t in TASKS_DB if t.id == 1)
    assert task.title == "Frotas atualizadas"
    assert task.status == "Em andamento"


@pytest.mark.integration
def test_change_status_to_complete(client):
    response = client.post("/task/complete/1", follow_redirects=True)
    assert response.status_code == 200
    task = next(t for t in TASKS_DB if t.id == 1)
    assert task.status == "Concluída"


@pytest.mark.integration
def test_delete_task(client):
    response = client.post("/task/delete/3", follow_redirects=True)
    assert response.status_code == 200
    assert not any(t.id == 3 for t in TASKS_DB)


@pytest.mark.integration
def test_search_tasks(client):
    response = client.get("/?search=motoristas")
    assert response.status_code == 200
    assert b"Cadastrar motoristas" in response.data
    assert b"Validar frotas de entrega" not in response.data


@pytest.mark.integration
def test_filter_tasks_by_priority_and_status(client):
    response = client.get("/?priority=Alta&status=Pendente")
    assert response.status_code == 200
    assert b"Validar frotas de entrega" in response.data
    assert b"Cadastrar motoristas" not in response.data


@pytest.mark.integration
def test_clear_filters_link(client):
    response = client.get("/?search=teste&priority=Alta")
    assert response.status_code == 200
    response = client.get("/")
    assert response.status_code == 200
    assert b"Validar frotas de entrega" in response.data
