import datetime
import json
import argparse

from task import Task

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

def main():
    filename = 'tasks.json'

    tasks = load_tasks(filename)

    parser = argparse.ArgumentParser(description="CLI app to track your tasks and manage your to-do list.")

    subparsers = parser.add_subparsers(dest='command', help='Subcommand to run')

    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('task_description', type=str, help='Description of the task')

    args = parser.parse_args()

    if args.command == 'add':
        new_id = get_next_id(tasks)

        task = Task(new_id, args.task_description, "todo", datetime.datetime.now().isoformat(), datetime.datetime.now().isoformat())

        tasks.append(task)

        save_tasks(filename, tasks)

        print(f"Task added successfully {task}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()