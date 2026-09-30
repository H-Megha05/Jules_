import unittest
import os
import tempfile
from task_tracker.manager import TaskManager


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()
        self.manager = TaskManager(filepath=self.temp_file.name)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_add_task(self):
        task = self.manager.add_task(
            title="Submit Report",
            description="Quarterly summary",
            category="Work",
            due_date="2026-10-05"
        )
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Submit Report")
        self.assertEqual(len(self.manager.tasks), 1)

    def test_persistence(self):
        self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")

        # Reload from same file
        new_manager = TaskManager(filepath=self.temp_file.name)
        self.assertEqual(len(new_manager.tasks), 2)
        self.assertEqual(new_manager.tasks[0].title, "Task 1")
        self.assertEqual(new_manager.tasks[1].title, "Task 2")

    def test_get_task(self):
        task = self.manager.add_task("Find me")
        retrieved = self.manager.get_task(task.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.title, "Find me")

        non_existent = self.manager.get_task(999)
        self.assertIsNone(non_existent)

    def test_list_tasks_and_filtering(self):
        t1 = self.manager.add_task("Work Task 1", category="Work")
        t2 = self.manager.add_task("Home Task 1", category="Home")
        t3 = self.manager.add_task("Work Task 2", category="Work")

        self.manager.complete_task(t1.id)

        all_tasks = self.manager.list_tasks()
        self.assertEqual(len(all_tasks), 3)

        completed_tasks = self.manager.list_tasks(status="completed")
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(completed_tasks[0].id, t1.id)

        pending_tasks = self.manager.list_tasks(status="pending")
        self.assertEqual(len(pending_tasks), 2)

        work_tasks = self.manager.list_tasks(category="Work")
        self.assertEqual(len(work_tasks), 2)

    def test_update_task(self):
        task = self.manager.add_task("Original Title")
        success = self.manager.update_task(task.id, title="Updated Title", category="Updated Cat")
        self.assertTrue(success)

        updated = self.manager.get_task(task.id)
        self.assertEqual(updated.title, "Updated Title")
        self.assertEqual(updated.category, "Updated Cat")

        fail = self.manager.update_task(999, title="Nowhere")
        self.assertFalse(fail)

    def test_delete_task(self):
        task = self.manager.add_task("To be deleted")
        self.assertEqual(len(self.manager.tasks), 1)

        success = self.manager.delete_task(task.id)
        self.assertTrue(success)
        self.assertEqual(len(self.manager.tasks), 0)

        fail = self.manager.delete_task(task.id)
        self.assertFalse(fail)

    def test_get_stats(self):
        t1 = self.manager.add_task("T1", category="CatA")
        t2 = self.manager.add_task("T2", category="CatB")
        self.manager.add_task("T3", category="CatA")
        self.manager.complete_task(t1.id)

        stats = self.manager.get_stats()
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["completed"], 1)
        self.assertEqual(stats["pending"], 2)
        self.assertEqual(stats["categories"]["CatA"], 2)
        self.assertEqual(stats["categories"]["CatB"], 1)


if __name__ == "__main__":
    unittest.main()
