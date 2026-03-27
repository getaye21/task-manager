#!/usr/bin/env python3
"""
Command-Line Task Manager with deadlines, priorities, and export to JSON/CSV.
"""

import argparse
import json
import csv
import sys
from datetime import datetime
from pathlib import Path

TASKS_FILE = Path("tasks.json")
PRIORITIES = {"high": 3, "medium": 2, "low": 1}
PRIORITY_NAMES = list(PRIORITIES.keys())

class Task:
    def __init__(self, id, description, deadline, priority, done=False):
        self.id = id
        self.description = description
        self.deadline = datetime.strptime(deadline, "%Y-%m-%d").date() if deadline else None
        self.priority = priority.lower()
        self.done = done

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "priority": self.priority,
            "done": self.done,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            description=data["description"],
            deadline=data.get("deadline"),
            priority=data.get("priority", "medium"),
            done=data.get("done", False),
        )

    def __repr__(self):
        deadline_str = self.deadline.isoformat() if self.deadline else "No deadline"
        status = "✓" if self.done else "✗"
        return f"[{self.id:2d}] {status} {self.description:30} | {deadline_str} | {self.priority:6}"

def load_tasks():
    if not TASKS_FILE.exists():
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Task.from_dict(t) for t in data]
    except (json.JSONDecodeError, KeyError):
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=2)

def add_task(description, deadline, priority):
    tasks = load_tasks()
    new_id = max([t.id for t in tasks], default=0) + 1
    task = Task(new_id, description, deadline, priority)
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added: {task.description}")

def list_tasks(filter_priority=None, sort_by=None, show_done=False):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    if filter_priority:
        tasks = [t for t in tasks if t.priority == filter_priority.lower()]
    if not show_done:
        tasks = [t for t in tasks if not t.done]
    if sort_by == "deadline":
        tasks.sort(key=lambda t: (t.deadline is None, t.deadline))
    elif sort_by == "priority":
        tasks.sort(key=lambda t: PRIORITIES[t.priority], reverse=True)
    for task in tasks:
        print(task)

def delete_task(task_id):
    tasks = load_tasks()
    original_len = len(tasks)
    tasks = [t for t in tasks if t.id != task_id]
    if len(tasks) == original_len:
        print(f"Task with ID {task_id} not found.")
    else:
        save_tasks(tasks)
        print(f"Task {task_id} deleted.")

def mark_done(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t.id == task_id:
            t.done = True
            save_tasks(tasks)
            print(f"Task {task_id} marked as done.")
            return
    print(f"Task with ID {task_id} not found.")

def export_tasks(format, output_file):
    tasks = load_tasks()
    if not tasks:
        print("No tasks to export.")
        return
    if format == "json":
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tasks], f, indent=2)
        print(f"Exported {len(tasks)} tasks to {output_file} (JSON).")
    elif format == "csv":
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Description", "Deadline", "Priority", "Done"])
            for t in tasks:
                writer.writerow([
                    t.id, t.description,
                    t.deadline.isoformat() if t.deadline else "",
                    t.priority, "Yes" if t.done else "No",
                ])
        print(f"Exported {len(tasks)} tasks to {output_file} (CSV).")
    else:
        print("Unsupported format. Use 'json' or 'csv'.")

def main():
    parser = argparse.ArgumentParser(description="Task Manager with deadlines and priorities.")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("description", help="Task description")
    parser_add.add_argument("--deadline", help="Deadline (YYYY-MM-DD)")
    parser_add.add_argument("--priority", choices=PRIORITY_NAMES, default="medium", help="Priority")
    parser_add.set_defaults(func=lambda args: add_task(args.description, args.deadline, args.priority))

    parser_list = subparsers.add_parser("list", help="List tasks")
    parser_list.add_argument("--filter", choices=PRIORITY_NAMES, dest="filter_priority", help="Filter by priority")
    parser_list.add_argument("--sort", choices=["deadline", "priority"], help="Sort by deadline or priority")
    parser_list.add_argument("--show-done", action="store_true", help="Show completed tasks")
    parser_list.set_defaults(func=lambda args: list_tasks(args.filter_priority, args.sort, args.show_done))

    parser_del = subparsers.add_parser("delete", help="Delete a task by ID")
    parser_del.add_argument("id", type=int, help="Task ID")
    parser_del.set_defaults(func=lambda args: delete_task(args.id))

    parser_done = subparsers.add_parser("done", help="Mark a task as completed")
    parser_done.add_argument("id", type=int, help="Task ID")
    parser_done.set_defaults(func=lambda args: mark_done(args.id))

    parser_export = subparsers.add_parser("export", help="Export tasks to JSON or CSV")
    parser_export.add_argument("--format", choices=["json", "csv"], required=True, help="Export format")
    parser_export.add_argument("--output", required=True, help="Output file name")
    parser_export.set_defaults(func=lambda args: export_tasks(args.format, args.output))

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
