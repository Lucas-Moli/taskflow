class Task:
    VALID_PRIORITIES = ["Alta", "Média", "Baixa"]
    VALID_STATUSES = ["Pendente", "Em andamento", "Concluída"]

    def __init__(self, task_id, title, description, priority="Média", status="Pendente"):
        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Prioridade inválida. Escolha entre: {self.VALID_PRIORITIES}")
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Status inválido. Escolha entre: {self.VALID_STATUSES}")
        self.id = int(task_id)
        self.title = str(title).strip()
        self.description = str(description).strip()
        self.priority = priority
        self.status = status

    def update(self, title, description, priority, status):
        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Prioridade inválida: {priority}")
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Status inválido: {status}")
        self.title = str(title).strip()
        self.description = str(description).strip()
        self.priority = priority
        self.status = status

    def complete(self):
        self.status = "Concluída"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
        }
