# Task Tracker CLI

A lightweight, clean, beginner-friendly command-line task management application built in Python. Effortlessly track your daily tasks, categories, due dates, and completion status right from your terminal with local JSON data persistence.

## Features

- **Add Tasks**: Specify titles, optional descriptions, custom categories, and due dates.
- **List & Filter Tasks**: View all tasks or filter by completion status (`pending`, `completed`) or category.
- **Update Tasks**: Modify task attributes dynamically.
- **Mark Complete**: Easily toggle task completion.
- **Delete Tasks**: Remove unwanted or old tasks.
- **Task Statistics**: View overall metrics and categorical breakdown.
- **Zero External Dependencies**: Powered entirely by Python standard library modules (`json`, `argparse`, `unittest`, `datetime`).

---

## Project Structure

```
.
├── main.py                 # CLI Entry point executable script
├── task_tracker/
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # CLI Argument parsing & command routing
│   ├── manager.py          # Core task manager & persistence logic
│   └── task.py             # Task data model definition
└── tests/
    ├── test_cli.py         # Unit tests for CLI functionality
    ├── test_manager.py     # Unit tests for TaskManager logic
    └── test_task.py        # Unit tests for Task model
```

---

## Getting Started

### Prerequisites

- Python 3.8 or higher installed on your system.

### Quick Start

Run `main.py` using Python:

```bash
python3 main.py --help
```

---

## Usage Examples

### 1. Adding a Task
```bash
python3 main.py add "Buy groceries" --description "Milk, Eggs, Bread" --category "Personal" --due "2026-10-05"
```

### 2. Listing Tasks
List all tasks:
```bash
python3 main.py list
```

Filter by completion status:
```bash
python3 main.py list --status pending
python3 main.py list --status completed
```

Filter by category:
```bash
python3 main.py list --category Personal
```

### 3. Marking a Task as Completed
```bash
python3 main.py complete 1
```

### 4. Updating a Task
```bash
python3 main.py update 1 --title "Buy organic groceries" --due "2026-10-06"
```

### 5. Viewing Task Statistics
```bash
python3 main.py stats
```

### 6. Deleting a Task
```bash
python3 main.py delete 1
```

### 7. Custom Data File Path
By default, tasks are saved to `tasks.json`. You can specify a custom file path using `--file`:
```bash
python3 main.py --file my_work_tasks.json add "Prepare presentation"
```

---

## Running Tests

The project includes unit tests written with Python's built-in `unittest` module.

Run all tests with:

```bash
python3 -m unittest discover -s tests
```

---

## License

This project is open-source and available under the MIT License.
