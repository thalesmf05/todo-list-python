import datetime
import json
from task import Task

class TaskManager:
    """
    Manages the list of Task objects.
    Handles core operations like add, remove, complete, display, and persistence.
    """
    def __init__(self):
        # Initializes an empty list to hold Task objects.
        self.tasks = []
    
    def get_tasks(self):
        """
        Returns the list of Task objects.
        """
        return self.tasks
    
    def add_task(self, task):
        """
        Adds a new Task to the task list.
        """
        self.tasks.append(task)

    def remove_task(self, index):
        """
        Removes a Task by its 1-based index.
        Returns the removed Task object if successful, or None if index is invalid.
        """
        try:
            removed = self.tasks.pop(index - 1)
            return removed
        except IndexError:
            return None

    def complete_task(self, index):
        """
        Marks a Task as completed by its 1-based index.
        Returns the updated Task if successful, or None if index is invalid.
        """
        try:
            self.tasks[index - 1].completed = True
            return self.tasks[index - 1]
        except IndexError:
            return None
    
    def show_tasks(self):
        """
        Prints all tasks to the terminal, displaying completion status.
        """
        if not self.tasks:
            print("No tasks in the list.")
            return
        
        for index, task in enumerate(self.tasks, start=1):
            status = "✅" if task.completed else "❌"
            print(f"{index}. {task.description} - {status}")
            
    def save_to_file(self, filename):
        """
        Serializes the list of tasks to a JSON file for persistence.
        """
        with open(filename, 'w') as f:
            tasks_dict = [task.to_dict() for task in self.tasks]
            json.dump(tasks_dict, f, indent=4)

    def load_from_file(self, filename):
        """
        Loads tasks from a JSON file and rebuilds the internal task list.
        If the file is not found, initializes an empty list.
        """
        try:
            with open(filename, 'r') as f:
                tasks_dict = json.load(f)
                self.tasks = [Task.from_dict(task) for task in tasks_dict]
        except FileNotFoundError:
            self.tasks = []



