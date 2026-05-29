import pytest

from src.models.task import Task
from src.repositories.task_repository import TaskRepository
from src.services.task_service import TaskService


@pytest.fixture
def service():
    repo = TaskRepository()
    repo.seed(
        [
            Task(1, "Entrega SP", "Carga para São Paulo", "Alta", "Pendente"),
            Task(2, "Entrega RJ", "Carga para Rio", "Média", "Concluída"),
        ],
        next_id=3,
    )
    return TaskService(repo)


@pytest.mark.unit
def test_list_with_search(service):
    tasks = service.list_tasks(search="rio")
    assert len(tasks) == 1
    assert tasks[0].title == "Entrega RJ"


@pytest.mark.unit
def test_list_with_priority_and_status(service):
    tasks = service.list_tasks(priority="Alta", status="Pendente")
    assert len(tasks) == 1
    assert tasks[0].id == 1


@pytest.mark.unit
def test_crud_lifecycle(service):
    created = service.create_task("Nova", "Desc", "Baixa")
    assert created.id == 3

    updated = service.update_task(3, "Nova 2", "Desc 2", "Alta", "Em andamento")
    assert updated.title == "Nova 2"

    completed = service.complete_task(3)
    assert completed.status == "Concluída"

    assert service.delete_task(3) is True
    assert service.get_task(3) is None


@pytest.mark.unit
def test_service_metadata(service):
    meta = service.metadata()
    assert Task.VALID_PRIORITIES == meta["priorities"]
    assert Task.VALID_STATUSES == meta["statuses"]
