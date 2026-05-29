import pytest

from src.app import create_app
from src.models.task import Task
from src.repositories.task_repository import task_repository


@pytest.fixture
def app():
    return create_app("testing")


@pytest.fixture
def client(app):
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def seed_tasks():
    """Repopula o repositório em memória com tarefas customizadas."""

    def _seed(tasks: list[Task], next_id: int | None = None) -> None:
        task_repository.seed(tasks, next_id=next_id)

    return _seed


@pytest.fixture
def default_tasks() -> list[Task]:
    return [
        Task(
            1,
            "Validar frotas de entrega",
            "Verificar caminhões pendentes.",
            "Alta",
            "Pendente",
        ),
        Task(
            2,
            "Cadastrar motoristas",
            "Novos colaboradores terceirizados.",
            "Média",
            "Em andamento",
        ),
        Task(
            3,
            "Revisar contratos",
            "Contratos vencidos em Salvador.",
            "Baixa",
            "Concluída",
        ),
    ]


@pytest.fixture(autouse=True)
def reset_repository(default_tasks, seed_tasks):
    seed_tasks(default_tasks, next_id=4)
    yield
