import json
import os
from typing import List, Optional, Dict, Any
from task_tracker.task import Task


class TaskManager:
    """Manages creation, retrieval, updating, deleting, and persistence of tasks."""

    def __init__(self, filepath: str = "tasks.json"):
        self.filepath = filepath
        self.tasks: List[Task] = []
        self._load_tasks()

    def _load_tasks(self) -> None:
        """Loads tasks from the JSON file if it exists."""
        if not os.path.exists(self.filepath):
            self.tasks = []
            return

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, OSError):
            self.tasks = []

    def _save_tasks(self) -> None:
        """Saves current tasks to the JSON file."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=2)

    def _get_next_id(self) -> int:
        """Generates the next available unique task ID."""
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1

    def add_task(self, title: str, description: str = "", category: str = "General", due_date: Optional[str] = None) -> Task:
        """Adds a new task and saves changes."""
        task_id = self._get_next_id()
        task = Task(id=task_id, title=title, description=description, category=category, due_date=due_date)
        self.tasks.append(task)
        self._save_tasks()
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieves a task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def list_tasks(self, status: Optional[str] = None, category: Optional[str] = None) -> List[Task]:
        """Lists tasks filtered by completion status ('completed', 'pending') and/or category."""
        result = self.tasks

        if status == "completed":
            result = [t for t in result if t.completed]
        elif status == "pending":
            result = [t for t in result if not t.completed]

        if category:
            result = [t for t in result if t.category.lower() == category.lower()]

        return result

    def complete_task(self, task_id: int) -> bool:
        """Marks a task as completed."""
        task = self.get_task(task_id)
        if task:
            task.completed = True
            self._save_tasks()
            return True
        return False

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None,
                    category: Optional[str] = None, due_date: Optional[str] = None) -> bool:
        """Updates attributes of an existing task."""
        task = self.get_task(task_id)
        if not task:
            return False

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if category is not None:
            task.category = category
        if due_date is not None:
            task.due_date = due_date

        self._save_tasks()
        return True

    def delete_task(self, task_id: int) -> bool:
        """Deletes a task by ID."""
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self._save_tasks()
            return True
        return False

    def get_stats(self) -> Dict[str, Any]:
        """Returns statistics about total, completed, and pending tasks."""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.completed)
        pending = total - completed
        categories = {}
        for t in self.tasks:
            categories[t.category] = categories.get(t.category, 0) + 1

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "categories": categories
        }
