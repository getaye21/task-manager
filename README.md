# Task Manager – Command-Line Tool

A simple Python command-line task manager that lets you add tasks with deadlines and priorities, list them, and export to JSON/CSV.

## Features

- ✅ Add tasks with **deadlines** (YYYY-MM-DD) and **priorities** (high/medium/low)
- ✅ List tasks, optionally filtered by priority or sorted by deadline/priority
- ✅ Mark tasks as done and delete tasks
- ✅ **Export** tasks to JSON or CSV files
- ✅ Full command-line argument support for quick management

## Installation

Clone the repository and run the script with Python 3.6+:

```bash
git clone https://github.com/your-username/task-manager.git
cd task-manager

##Usage

# Add a task
python task_manager.py add "Write report" --deadline 2025-12-31 --priority high

# List pending tasks
python task_manager.py list

# List all tasks sorted by deadline
python task_manager.py list --show-done --sort deadline

# Mark a task as done
python task_manager.py done 1

# Delete a task
python task_manager.py delete 2

# Export to CSV
python task_manager.py export --format csv --output tasks.csv

# Export to JSON
python task_manager.py export --format json --output tasks.json
