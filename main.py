from v2.utils import show_main_menu
from v2.task_manager import TaskManager


if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.load_from_file("tasks.json")
    
    
    show_main_menu(task_manager)