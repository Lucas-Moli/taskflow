from src.models.task import Task
from src.repositories.task_repository import TaskRepository, task_repository


class TaskService:
    """Regras de negócio e orquestração do domínio de tarefas."""

    def __init__(self, repository: TaskRepository):
        self._repository = repository

    def list_tasks(
        self,
        search: str = "",
        priority: str = "",
        status: str = "",
    ) -> list[Task]:
        return self._repository.filter(
            search=search.strip(),
            priority=priority.strip(),
            status=status.strip(),
        )

    def get_task(self, task_id: int) -> Task | None:
        return self._repository.find_by_id(task_id)

    def create_task(
        self,
        title: str,
        description: str,
        priority: str = "Média",
        status: str = "Pendente",
    ) -> Task:
        return self._repository.create(title, description, priority, status)

    def update_task(
        self,
        task_id: int,
        title: str,
        description: str,
        priority: str,
        status: str,
    ) -> Task | None:
        return self._repository.update(task_id, title, description, priority, status)

    def complete_task(self, task_id: int) -> Task | None:
        return self._repository.complete(task_id)

    def delete_task(self, task_id: int) -> bool:
        return self._repository.delete(task_id)

    @staticmethod
    def metadata() -> dict:
        return {
            "priorities": Task.VALID_PRIORITIES,
            "statuses": Task.VALID_STATUSES,
        }


task_service = TaskService(task_repository)
