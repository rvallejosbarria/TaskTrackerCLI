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
                return [Task.from_dict(item) for item in data]
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
        return max(task.id for task in tasks) + 1
    else:
        return 1

def save_tasks(filename: str, tasks: list) -> None:
    try:
        with open(filename, "w") as file:
            json.dump([task.to_dict() for task in tasks], file, indent=4)
    except IOError:
        print(f"An I/O error occurred while trying to write to the file {filename}.")
    except TypeError as e:
        print("Failed to serialize object to JSON: {e}")

def find_task_by_id(tasks: list, task_id: int) -> Optional[Task]:
    for task in tasks:
        if task.id == task_id:
            return task
    return None

def main():
    filename = 'tasks.json'

    tasks = load_tasks(filename)

    parser = argparse.ArgumentParser(description="CLI app to track your tasks and manage your to-do list.")

    subparsers = parser.add_subparsers(dest='command', help='Subcommand to run')

    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('task_description', type=str, help='Description of the task')

    update_parser = subparsers.add_parser('update', help='Update a task')
    update_parser.add_argument('task_id', type=int, help='ID of the task')
    update_parser.add_argument('new_task_description', type=str, help='New description of the task')

    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('task_id', type=int, help='ID of the task')

    mark_in_progress_parser = subparsers.add_parser('mark-in-progress',
                                                    help='Change the status of a task to \'In progress\'')
    mark_in_progress_parser.add_argument('task_id', type=int, help='ID of the task')

    mark_done_parser = subparsers.add_parser('mark-done',
                                                    help='Change the status of a task to \'Done\'')
    mark_done_parser.add_argument('task_id', type=int, help='ID of the task')

    list_parser = subparsers.add_parser('list', help='List all tasks')
    list_parser.add_argument('--status', type=str, help='List tasks by status')

    args = parser.parse_args()

    if args.command == 'add':
        new_id = get_next_id(tasks)

        task = Task(new_id, args.task_description, "todo", datetime.datetime.now().isoformat(), datetime.datetime.now().isoformat())

        tasks.append(task)

        save_tasks(filename, tasks)

        print(f"Task added successfully {task}")
    elif args.command == 'update':
        found_task = find_task_by_id(tasks, args.task_id)

        if found_task:
            found_task.description = args.new_task_description
            found_task.updated_at = datetime.datetime.now().isoformat()

            save_tasks(filename, tasks)

            print("Task updated successfully")
        else:
            print(f"No task found with ID {args.task_id}")
    elif args.command == 'delete':
        found_task = find_task_by_id(tasks, args.task_id)

        if found_task:
            tasks.remove(found_task)

            save_tasks(filename, tasks)

            print("Task deleted successfully")
        else:
            print(f"No task found with ID {args.task_id}")
    elif args.command == 'mark-in-progress':
        found_task = find_task_by_id(tasks, args.task_id)

        if found_task:
            found_task.status = 'in-progress'
            found_task.updated_at = datetime.datetime.now().isoformat()

            save_tasks(filename, tasks)

            print("Task updated successfully")
        else:
            print(f"No task found with ID {args.task_id}")
    elif args.command == 'mark-done':
        found_task = find_task_by_id(tasks, args.task_id)

        if found_task:
            found_task.status = 'done'
            found_task.updated_at = datetime.datetime.now().isoformat()

            save_tasks(filename, tasks)

            print("Task updated successfully")
        else:
            print(f"No task found with ID {args.task_id}")
    elif args.command == 'list':
        if args.status:
            for task in tasks:
                if task.status == args.status:
                    print(f"{task.description}")
        else:
            for task in tasks:
                print(f"{task.description}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()