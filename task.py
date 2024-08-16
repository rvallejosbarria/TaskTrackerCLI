class Task:
    def __init__(self, task_id: int, description: str, status: str, created_at: str, updated_at: str) -> None:
        self.id = task_id
        self.description = description
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        return f"\"{self.description}\" (ID: {self.id}) created at: {self.created_at}"

    @staticmethod
    def from_dict(data):
        return Task(data["id"], data["description"], data["status"], data["created_at"], data["updated_at"])