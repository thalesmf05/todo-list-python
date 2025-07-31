from utils import show_main_menu
from task_manager import TaskManager
from utils import json_path

# Entry point for the application.
# Initializes the TaskManager, loads tasks from file, and starts the main menu loop.

if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.load_from_file(json_path)
    
    show_main_menu(task_manager)
