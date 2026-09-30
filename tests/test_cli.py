import unittest
import os
import tempfile
import io
import sys
from task_tracker.cli import run_cli


class TestCLI(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def run_command(self, args_list):
        full_args = ["--file", self.temp_file.name] + args_list
        old_stdout = sys.stdout
        captured_output = io.StringIO()
        try:
            sys.stdout = captured_output
            exit_code = run_cli(full_args)
        finally:
            sys.stdout = old_stdout
        return exit_code, captured_output.getvalue()

    def test_add_and_list_cli(self):
        exit_code, output = self.run_command(["add", "Buy Milk", "-d", "2 gallons", "-c", "Groceries"])
        self.assertEqual(exit_code, 0)
        self.assertIn("Task successfully added with ID #1", output)

        exit_code, output = self.run_command(["list"])
        self.assertEqual(exit_code, 0)
        self.assertIn("Buy Milk", output)
        self.assertIn("Groceries", output)

    def test_complete_and_stats_cli(self):
        self.run_command(["add", "Task 1"])
        exit_code, output = self.run_command(["complete", "1"])
        self.assertEqual(exit_code, 0)
        self.assertIn("marked as completed", output)

        exit_code, output = self.run_command(["stats"])
        self.assertEqual(exit_code, 0)
        self.assertIn("Total Tasks:     1", output)
        self.assertIn("Completed Tasks: 1", output)

    def test_update_and_delete_cli(self):
        self.run_command(["add", "Old Title"])
        exit_code, output = self.run_command(["update", "1", "--title", "New Title"])
        self.assertEqual(exit_code, 0)
        self.assertIn("updated successfully", output)

        exit_code, output = self.run_command(["delete", "1"])
        self.assertEqual(exit_code, 0)
        self.assertIn("deleted successfully", output)


if __name__ == "__main__":
    unittest.main()
