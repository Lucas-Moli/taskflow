from src.models.task import Task


class TaskRepository:
    """Persistência em memória das tarefas."""

    def __init__(self):
        self.storage: list[Task] = []
        self._id_counter = 1

    def seed(self, tasks: list[Task], next_id: int | None = None) -> None:
        self.storage.clear()
        self.storage.extend(tasks)
        if next_id is not None:
            self._id_counter = next_id
        elif tasks:
            self._id_counter = max(t.id for t in tasks) + 1
        else:
            self._id_counter = 1

    def _next_id(self) -> int:
        current = self._id_counter
        self._id_counter += 1
        return current

    def get_all(self) -> list[Task]:
        return list(self.storage)

    def find_by_id(self, task_id: int) -> Task | None:
        return next((t for t in self.storage if t.id == task_id), None)

    def create(self, title: str, description: str, priority: str, status: str = "Pendente") -> Task:
        task = Task(self._next_id(), title, description, priority, status)
        self.storage.append(task)
        return task

    def update(
        self,
        task_id: int,
        title: str,
        description: str,
        priority: str,
        status: str,
    ) -> Task | None:
        task = self.find_by_id(task_id)
        if not task:
            return None
        task.update(title, description, priority, status)
        return task

    def complete(self, task_id: int) -> Task | None:
        task = self.find_by_id(task_id)
        if not task:
            return None
        task.complete()
        return task

    def delete(self, task_id: int) -> bool:
        task = self.find_by_id(task_id)
        if not task:
            return False
        self.storage.remove(task)
        return True

    def filter(
        self,
        search: str = "",
        priority: str = "",
        status: str = "",
    ) -> list[Task]:
        result = self.storage
        if search:
            query = search.lower()
            result = [
                t
                for t in result
                if query in t.title.lower() or query in t.description.lower()
            ]
        if priority:
            result = [t for t in result if t.priority == priority]
        if status:
            result = [t for t in result if t.status == status]
        return list(result)


def _default_tasks() -> list[Task]:
    return [
        Task(
            1,
            "Otimizar Rotas de Entrega",
            "Implementar algoritmo de Dijkstra para reduzir tempo de frete.",
            "Alta",
            "Em andamento",
        ),
        Task(
            2,
            "Integrar API de Rastreamento",
            "Conectar o sistema com a API dos Correios e transportadoras parceiras.",
            "Média",
            "Pendente",
        ),
        Task(
            3,
            "Homologar Relatório Financeiro",
            "Validar fechamento mensal de gastos com combustível.",
            "Baixa",
            "Concluída",
        ),
    ]


task_repository = TaskRepository()
task_repository.seed(_default_tasks(), next_id=4)

# Compatibilidade com testes e imports legados
TASKS_DB = task_repository.storage
