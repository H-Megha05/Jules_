import unittest
from task_tracker.task import Task


class TestTask(unittest.TestCase):

    def test_task_creation_defaults(self):
        task = Task(id=1, title="Test Task")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "")
        self.assertEqual(task.category, "General")
        self.assertIsNone(task.due_date)
        self.assertFalse(task.completed)
        self.assertIsNotNone(task.created_at)

    def test_task_to_dict_and_from_dict(self):
        task = Task(
            id=2,
            title="Buy groceries",
            description="Milk, eggs, bread",
            category="Personal",
            due_date="2026-10-01",
            completed=True,
            created_at="2026-09-30 12:00:00"
        )
        task_dict = task.to_dict()
        self.assertEqual(task_dict["id"], 2)
        self.assertEqual(task_dict["title"], "Buy groceries")
        self.assertEqual(task_dict["completed"], True)

        reconstructed_task = Task.from_dict(task_dict)
        self.assertEqual(reconstructed_task.id, task.id)
        self.assertEqual(reconstructed_task.title, task.title)
        self.assertEqual(reconstructed_task.description, task.description)
        self.assertEqual(reconstructed_task.category, task.category)
        self.assertEqual(reconstructed_task.due_date, task.due_date)
        self.assertEqual(reconstructed_task.completed, task.completed)
        self.assertEqual(reconstructed_task.created_at, task.created_at)

    def test_task_repr(self):
        task_pending = Task(id=1, title="Pending Task", category="Work")
        task_completed = Task(id=2, title="Done Task", category="Work", completed=True)

        self.assertIn("[ ] Task #1: Pending Task", repr(task_pending))
        self.assertIn("[✓] Task #2: Done Task", repr(task_completed))


if __name__ == "__main__":
    unittest.main()
