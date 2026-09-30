import datetime

class Task:
    """Represents an individual task in the task tracker."""

    def __init__(self, id: int, title: str, description: str = "", category: str = "General",
                 due_date: str = None, completed: bool = False, created_at: str = None):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.completed = completed
        self.created_at = created_at if created_at else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        """Converts the task instance to a dictionary for JSON storage."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "completed": self.completed,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Creates a Task instance from a dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            category=data.get("category", "General"),
            due_date=data.get("due_date"),
            completed=data.get("completed", False),
            created_at=data.get("created_at")
        )

    def __repr__(self) -> str:
        status = "✓" if self.completed else " "
        return f"[{status}] Task #{self.id}: {self.title} (Category: {self.category})"
