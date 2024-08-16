class Task:
    def __init__(self, task_id: int, description: str, status: str, created_at: str, updated_at: str) -> None:
        self.id = task_id
        self.description = description
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at