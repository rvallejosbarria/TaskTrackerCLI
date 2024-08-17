import sys
import datetime
import json
import argparse

from task import Task
from typing import Optional

def load_tasks(filename: str):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            if isinstance(data, list):
                return [Task.from_dict(item) for item in data]  # Convert dictionaries to Task objects
            else:
                raise TypeError("Expected a list of dictionaries in the JSON file")
    except FileNotFoundError:
        print(f"{filename} not found. Starting with an empty list.")
        return []
    except IOError:
        print(f"An I/O error occurred while trying to read the file {filename}.")
        return []
    except json.JSONDecodeError:
        print(f"{filename} is empty or contains invalid JSON. Starting with an empty list.")
        return []

def get_next_id(tasks: list) -> int:
    if tasks:
        return max(task.id for task in tasks) + 1  # Increment the highest existing ID by 1
    else:
        return 1  # If no tasks exist, start with ID 1

def save_tasks(filename: str, tasks: list) -> None:
    try:
        with open(filename, "w") as file:
            json.dump([task.to_dict() for task in tasks], file, indent=4)  # Convert Task objects to dictionaries and save as JSON
    except IOError:
        print(f"An I/O error occurred while trying to write to the file {filename}.")
    except TypeError as e:
        print("Failed to serialize object to JSON: {e}")

def find_task_by_id(tasks: list, task_id: int) -> Optional[Task]:
    for task in tasks:
        if task.id == task_id:
            return task
    return None

def print_colored(text, color, end='\n'):
    colors = {
        'High': '\x1b[31m', # Red
        'Medium': '\x1b[33m', # Yellow
        'Low': '\x1b[32m',  # Green
    }
    reset = '\x1b[0m'
    sys.stdout.write(colors.get(color, '') + text + reset + end)

def main():
    filename = 'tasks.json'  # File where tasks are stored

    tasks = load_tasks(filename)  # Load existing tasks from the file

    parser = argparse.ArgumentParser(description="CLI app to track your tasks and manage your to-do list.")

    # Define subcommands for various operations
    subparsers = parser.add_subparsers(dest='command', help='Subcommand to run')

    # Subcommand for adding a new task
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('task_description', type=str, help='Description of the task')

    add_parser.add_argument('--priority', type=str, choices=['Low', 'Medium', 'High'], default='Low',
                            help='Priority of the task')
    add_parser.add_argument('--due-date', type=str, help='Due date of the task')

    # Subcommand for updating an existing task
    update_parser = subparsers.add_parser('update', help='Update a task')
    update_parser.add_argument('task_id', type=int, help='ID of the task')
    update_parser.add_argument('new_task_description', type=str, help='New description of the task')

    # Subcommand for deleting a task
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('task_id', type=int, help='ID of the task')

    # Subcommand for marking a task as 'In progress'
    mark_in_progress_parser = subparsers.add_parser('mark-in-progress',
                                                    help='Change the status of a task to \'In progress\'')
    mark_in_progress_parser.add_argument('task_id', type=int, help='ID of the task')

    # Subcommand for marking a task as 'Done'
    mark_done_parser = subparsers.add_parser('mark-done',
                                                    help='Change the status of a task to \'Done\'')
    mark_done_parser.add_argument('task_id', type=int, help='ID of the task')

    # Subcommand for listing tasks
    list_parser = subparsers.add_parser('list', help='List all tasks')
    list_parser.add_argument('--status', type=str, help='List tasks by status')
    list_parser.add_argument('--due-date', type=str, help='List tasks by due date')

    args = parser.parse_args()  # Parse the command-line arguments

    if args.command == 'add':
        new_id = get_next_id(tasks) # Generate a new task ID

        # Create a new task and append it to the list
        task = Task(new_id, args.task_description, "todo", args.priority, args.due_date, datetime.datetime.now().isoformat(),
                    datetime.datetime.now().isoformat())
        tasks.append(task)

        save_tasks(filename, tasks) # Save tasks to the file

        print(f"Task added successfully {task}")
    elif args.command == 'update':
        found_task = find_task_by_id(tasks, args.task_id)  # Find the task by ID

        if found_task:
            # Update the task's description and timestamp
            found_task.description = args.new_task_description
            found_task.updated_at = datetime.datetime.now().isoformat()

            save_tasks(filename, tasks)  # Save changes to the file

            print("Task updated successfully")
        else:
            print(f"No task found with ID {args.task_id}")
    elif args.command == 'delete':
        found_task = find_task_by_id(tasks, args.task_id)  # Find the task by ID

        if found_task:
            tasks.remove(found_task)  # Remove the task from the list

            save_tasks(filename, tasks)  # Save changes to the file

            print("Task deleted successfully")
        else:
            print(f"No task found with ID {args.task_id}")
    elif args.command == 'mark-in-progress':
        found_task = find_task_by_id(tasks, args.task_id)  # Find the task by ID

        if found_task:
            # Update the task's status and timestamp
            found_task.status = 'in-progress'
            found_task.updated_at = datetime.datetime.now().isoformat()

            save_tasks(filename, tasks)  # Save changes to the file

            print("Task updated successfully")
        else:
            print(f"No task found with ID {args.task_id}")
    elif args.command == 'mark-done':
        found_task = find_task_by_id(tasks, args.task_id)  # Find the task by ID

        if found_task:
            # Update the task's status and timestamp
            found_task.status = 'done'
            found_task.updated_at = datetime.datetime.now().isoformat()

            save_tasks(filename, tasks)  # Save changes to the file

            print("Task updated successfully")
        else:
            print(f"No task found with ID {args.task_id}")
    elif args.command == 'list':
        priority_order = {
            "Low": 1,
            "Medium": 2,
            "High": 3
        }

        # Sort tasks by priority in ascending order
        tasks.sort(key=lambda  task: priority_order[task.priority], reverse=True)

        # List tasks based on status or all tasks if no status is specified
        for task in tasks:
            if (not args.status or task.status == args.status) and (not args.due_date or task.due_date == args.due_date):
                print_colored(task.description, color=task.priority)
    else:
        parser.print_help() # Print help message if no valid subcommand is provided

if __name__ == "__main__":
    main()