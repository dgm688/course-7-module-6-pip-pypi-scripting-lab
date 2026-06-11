from datetime import datetime
import requests
import csv
import argparse


def generate_log(data):
    if not isinstance(data, list):
        raise ValueError("Input must be a list")
    filename = f"log_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(filename, "w") as file:
        for entry in data:
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
    return {}


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


if __name__ == "__main__":
    log_data = ["User logged in", "User updated profile", "Report exported"]
    generate_log(log_data)
    fetch_data()
    manager = TaskManager("Alice")
    manager.add_task("Write report")
    manager.add_task("Send email")
    manager.complete_task("Write report")
    manager.show_tasks()
