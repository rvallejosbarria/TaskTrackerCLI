class Task:
    def __init__(self, task_id: int, description: str, status: str, priority: str, due_date: str, created_at: str, updated_at: str) -> None:
        self.id = task_id
        self.description = description
        self.status = status
        self.priority = priority
        self.due_date = due_date
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        return f"\"{self.description}\" (ID: {self.id}) created at: {self.created_at}"

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @staticmethod
    def from_dict(data):
        return Task(data["id"], data["description"], data["status"], data["priority"], data["due_date"], data["created_at"], data["updated_at"])
