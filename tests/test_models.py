import pytest

from src.models.task import Task


@pytest.mark.unit
def test_task_defaults():
    task = Task(1, "  Título  ", "  Descrição  ")
    assert task.priority == "Média"
    assert task.status == "Pendente"
    assert task.title == "Título"
    assert task.description == "Descrição"


@pytest.mark.unit
def test_task_invalid_priority():
    with pytest.raises(ValueError, match="Prioridade inválida"):
        Task(1, "T", "D", "Critica")


@pytest.mark.unit
def test_task_invalid_status():
    with pytest.raises(ValueError, match="Status inválido"):
        Task(1, "T", "D", "Média", "Cancelada")


@pytest.mark.unit
def test_task_update_validates_fields():
    task = Task(1, "A", "B")
    with pytest.raises(ValueError):
        task.update("A", "B", "Inválida", "Pendente")


@pytest.mark.unit
def test_task_complete_changes_status():
    task = Task(1, "A", "B", status="Em andamento")
    task.complete()
    assert task.status == "Concluída"


@pytest.mark.unit
def test_task_to_dict():
    task = Task(10, "Frete", "SP-RJ", "Alta", "Pendente")
    assert task.to_dict() == {
        "id": 10,
        "title": "Frete",
        "description": "SP-RJ",
        "priority": "Alta",
        "status": "Pendente",
    }
