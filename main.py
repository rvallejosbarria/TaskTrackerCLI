import json

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

def main():
    filename = 'tasks.json'
    tasks = load_tasks(filename)

if __name__ == "__main__":
    main()