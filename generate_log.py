"""
Automation Tool - Lab Solution
"""

import argparse
import csv
import requests
from datetime import datetime


class TaskManager:
    def __init__(self, username):
        self.username = username
        self.tasks = []

    def add_task(self, task_name):
        task = {"task": task_name, "status": "pending"}
        self.tasks.append(task)
        print(f"[{self.username}] Task added: '{task_name}'")

    def complete_task(self, task_name):
        for task in self.tasks:
            if task["task"] == task_name:
                task["status"] = "complete"
                print(f"[{self.username}] Task completed: '{task_name}'")
                return
        print(f"Task '{task_name}' not found.")

    def show_tasks(self):
        if not self.tasks:
            print("No tasks yet.")
            return
        print(f"\nTasks for {self.username}:")
        for i, task in enumerate(self.tasks, 1):
            print(f"  {i}. {task['task']} [{task['status']}]")


def write_log():
    log_data = ["User logged in", "User updated profile", "Report exported"]
    filename = f"log_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(filename, "w") as file:
        for entry in log_data:
            file.write(f"{entry}\n")
    print(f"Log written to {filename}")
    return filename


def fetch_data():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    if response.status_code == 200:
        post = response.json()
        print("Fetched Post Title:", post.get("title", "No title found"))
        with open("fetched_data.csv", "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["userId", "id", "title", "body"])
            writer.writeheader()
            writer.writerow(post)
        print("Data saved to fetched_data.csv")
        return post
    else:
        print("Failed to fetch data.")
        return {}


def build_cli():
    parser = argparse.ArgumentParser(description="Simple CLI Task Manager")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add-task")
    add_parser.add_argument("--user", required=True)
    add_parser.add_argument("--task", required=True)

    complete_parser = subparsers.add_parser("complete-task")
    complete_parser.add_argument("--user", required=True)
    complete_parser.add_argument("--task", required=True)

    subparsers.add_parser("fetch")
    subparsers.add_parser("log")

    return parser


if __name__ == "__main__":
    parser = build_cli()
    args = parser.parse_args()

    manager = TaskManager(getattr(args, "user", "default_user"))

    if args.command == "add-task":
        manager.add_task(args.task)

    elif args.command == "complete-task":
        manager.add_task(args.task)
        manager.complete_task(args.task)

    elif args.command == "fetch":
        fetch_data()

    elif args.command == "log":
        write_log()

    else:
        print("=== Running full demo ===\n")
        write_log()
        print()
        fetch_data()
        print()
        manager = TaskManager("Alice")
        manager.add_task("Write report")
        manager.add_task("Send email")
        manager.complete_task("Write report")
        manager.show_tasks()
