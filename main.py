import datetime

from task import Task

def main():
    task = Task(1, "Hello from the task instance", "todo", datetime.datetime.now().isoformat(), datetime.datetime.now().isoformat())
    print(f"Created successfully task {task}")

if __name__ == "__main__":
    main()