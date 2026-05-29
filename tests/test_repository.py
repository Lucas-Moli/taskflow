import pytest

from src.models.task import Task
from src.repositories.task_repository import TaskRepository


@pytest.fixture
def repo():
    repository = TaskRepository()
    repository.seed(
        [
            Task(1, "Alpha", "Primeira", "Alta", "Pendente"),
            Task(2, "Beta", "Segunda", "Baixa", "Concluída"),
        ],
        next_id=3,
    )
    return repository


@pytest.mark.unit
def test_repository_create_and_find(repo):
    created = repo.create("Gamma", "Terceira", "Média")
    assert created.id == 3
    found = repo.find_by_id(3)
    assert found is not None
    assert found.title == "Gamma"


@pytest.mark.unit
def test_repository_filter_by_search(repo):
    results = repo.filter(search="beta")
    assert len(results) == 1
    assert results[0].title == "Beta"


@pytest.mark.unit
def test_repository_filter_combined(repo):
    results = repo.filter(priority="Alta", status="Pendente")
    assert len(results) == 1
    assert results[0].id == 1


@pytest.mark.unit
def test_repository_delete_missing_returns_false(repo):
    assert repo.delete(999) is False


@pytest.mark.unit
def test_repository_update_missing_returns_none(repo):
    assert repo.update(999, "X", "Y", "Alta", "Pendente") is None
