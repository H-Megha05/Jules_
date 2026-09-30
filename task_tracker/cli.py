import argparse
import sys
from typing import List, Optional
from task_tracker.manager import TaskManager


def build_parser() -> argparse.ArgumentParser:
    """Builds and returns the ArgumentParser for CLI commands."""
    parser = argparse.ArgumentParser(
        description="Task Tracker CLI - Manage your daily tasks efficiently from the terminal.",
        prog="task-tracker"
    )
    parser.add_argument("--file", "-f", default="tasks.json", help="Path to JSON storage file (default: tasks.json)")

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Add task
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Title of the task")
    add_parser.add_argument("--description", "-d", default="", help="Detailed description")
    add_parser.add_argument("--category", "-c", default="General", help="Task category")
    add_parser.add_argument("--due", help="Due date (e.g. YYYY-MM-DD)")

    # List tasks
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--status", choices=["completed", "pending"], help="Filter by status")
    list_parser.add_argument("--category", "-c", help="Filter by category")

    # Complete task
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("id", type=int, help="Task ID")

    # Update task
    update_parser = subparsers.add_parser("update", help="Update an existing task")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("--title", "-t", help="New title")
    update_parser.add_argument("--description", "-d", help="New description")
    update_parser.add_argument("--category", "-c", help="New category")
    update_parser.add_argument("--due", help="New due date")

    # Delete task
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    # Stats
    subparsers.add_parser("stats", help="Display task statistics")

    return parser


def run_cli(args: Optional[List[str]] = None) -> int:
    """Main CLI execution logic."""
    parser = build_parser()
    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        parser.print_help()
        return 0

    manager = TaskManager(filepath=parsed_args.file)

    if parsed_args.command == "add":
        task = manager.add_task(
            title=parsed_args.title,
            description=parsed_args.description,
            category=parsed_args.category,
            due_date=parsed_args.due
        )
        print(f"Task successfully added with ID #{task.id}: '{task.title}'")

    elif parsed_args.command == "list":
        tasks = manager.list_tasks(status=parsed_args.status, category=parsed_args.category)
        if not tasks:
            print("No tasks found.")
        else:
            print(f"\nFound {len(tasks)} task(s):")
            print("-" * 60)
            for task in tasks:
                status_str = "[Completed]" if task.completed else "[Pending]"
                due_str = f" | Due: {task.due_date}" if task.due_date else ""
                desc_str = f"\n    Description: {task.description}" if task.description else ""
                print(f"#{task.id:<3} {status_str:<12} [{task.category}] {task.title}{due_str}{desc_str}")
            print("-" * 60)

    elif parsed_args.command == "complete":
        if manager.complete_task(parsed_args.id):
            print(f"Task #{parsed_args.id} marked as completed.")
        else:
            print(f"Error: Task #{parsed_args.id} not found.")
            return 1

    elif parsed_args.command == "update":
        success = manager.update_task(
            task_id=parsed_args.id,
            title=parsed_args.title,
            description=parsed_args.description,
            category=parsed_args.category,
            due_date=parsed_args.due
        )
        if success:
            print(f"Task #{parsed_args.id} updated successfully.")
        else:
            print(f"Error: Task #{parsed_args.id} not found.")
            return 1

    elif parsed_args.command == "delete":
        if manager.delete_task(parsed_args.id):
            print(f"Task #{parsed_args.id} deleted successfully.")
        else:
            print(f"Error: Task #{parsed_args.id} not found.")
            return 1

    elif parsed_args.command == "stats":
        stats = manager.get_stats()
        print("\nTask Tracker Statistics:")
        print("=" * 30)
        print(f"Total Tasks:     {stats['total']}")
        print(f"Completed Tasks: {stats['completed']}")
        print(f"Pending Tasks:   {stats['pending']}")
        if stats['categories']:
            print("\nCategories Breakdown:")
            for cat, count in stats['categories'].items():
                print(f"  - {cat}: {count}")
        print("=" * 30)

    return 0
