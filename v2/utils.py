from ast import Return
import datetime
from .task import Task
from .task_manager import TaskManager
from v2 import task
from wcwidth import wcswidth

from v2 import task_manager

def pad_cell(text, width):
    """Alinha texto centralizado de acordo com a largura VISUAL (não só len())."""
    visual_width = wcswidth(text)
    pad = width - visual_width
    left = pad // 2
    right = pad - left
    return " " * left + text + " " * right

# Valide user input          
def validate_user_input(user_input, max_index, min_index, context):
    try:
        user_input = int(user_input)
        if not (min_index <= user_input <= max_index):
                if context != "remove":
                    print(f"Invalid option. Please only number beetwen {min_index} - {max_index}.") 
                    return None
                        
                                 
    except ValueError:
        if context != "remove": #if been used in remove, it will not print the message
            print(f"Invalid option. Please only number beetwen {min_index} - {max_index}.")
        return None
    else:
        return user_input
        
# Display a list of options and return the chosen one
def show_options(prompt, question, options):
    if prompt is not None:
        print(prompt)
    for idx, opt in enumerate(options, 1):
        print(f"{idx}. {opt}")
    while True:
        choice = input(question)
        validated = validate_user_input(choice, len(options), 1, "show_options")
        if validated is not None:
            return validated


        
# Validate user input for menu options
def show_main_menu(task_manager):
       
    while True:
        to_do_list = task_manager.get_tasks()
        option = show_options("----------- Menu -----------", "Choose one: ",["View Tasks", "Add Task", "Complete Task", "Remove Task", "Exit"])
        
        if option == 1:
            print_task_table(task_manager.get_tasks())

            option = show_options(None,"What next? ",["Add task","Complete Task", "Remove Task", "Go back"])
            if option == 1:
                handle_add(task_manager)
            elif option == 2:
                handle_complete(task_manager)
            elif option == 3:
                handle_remove(task_manager)
            elif option == 4:
                show_main_menu(task_manager)

        elif option == 2:
            handle_add(task_manager)
        elif option == 3:
            handle_complete(task_manager)
        elif option == 4:
            handle_remove(task_manager) 
        elif option == 5:
            print("exit app") #TODO exit app

def print_task_table(tasks):
    # Defina as larguras das colunas (ajuste se quiser)
    col_widths = [4, 19, 8, 21, 10]  # No, Task, Status, Created at, Deadline
    table_width = sum(col_widths) + len(col_widths) + 1

    # 1. Título centralizado
    title = "TO-DO LIST MANAGER"
    print("\n" + title.center(table_width))

    # 2. Linha do topo
    print("+" + "+".join("-" * w for w in col_widths) + "+")

    # 3. Cabeçalho
    headers = ["No", "Task", "Status", "Created at", "Deadline"]
    header_cells = [pad_cell(h, w) for h, w in zip(headers, col_widths)]
    print("|" + "|".join(header_cells) + "|")

    # 4. Linha separadora
    print("+" + "+".join("-" * w for w in col_widths) + "+")

    # 5. Corpo da tabela
    if not tasks:
        empty = "No tasks found."
        print("|" + pad_cell(empty, table_width - 2) + "|")
    else:
        for idx, task in enumerate(tasks, 1):
            status = "❌" if not task.completed else "✅"
            created = task.time.strftime("%Y-%m-%d %H:%M")
            deadline = getattr(task, "deadline", "---") or "---"
            cells = [
                pad_cell(str(idx), col_widths[0]),
                pad_cell(task.description[:col_widths[1]], col_widths[1]),
                pad_cell(status, col_widths[2]),
                pad_cell(created, col_widths[3]),
                pad_cell(str(deadline), col_widths[4])
            ]
            print("|" + "|".join(cells) + "|")
    # 6. Rodapé
    print("+" + "+".join("-" * w for w in col_widths) + "+")



def handle_add(task_manager):
      while True:
        new_task = input("Enter a task: ").strip()
        
        if new_task == "":
            print("You must enter something!")
            continue

        while True:
            exists = any(task.description.lower().strip() == new_task.lower() for task in task_manager.get_tasks())
            
            if exists:
                print("This task is already on the list.")
                retry =  input("Press ENTER to go back or type a new task: ").strip()

                if retry == "":
                   return 
                else:
                    new_task = retry
                    continue
            
            else:
                try:
                    task = Task(new_task, False, datetime.datetime.now())
                    task_manager.add_task(task)
                    task_manager.save_to_file("tasks.json")
                    print(f"Task '{new_task}' addded!")
                    
                except Exception as e:
                    print(f"Error while adding the task : {e}")
                else:
                    option = show_options(None, "What next? ", ["Add another", "View list", "Back to main menu"])
                    if option == 1:
                        handle_add(task_manager)
                    elif option == 2: 
                        print("Fazer parte do view")
                    elif option == 3:
                        return

def handle_remove(task_manager):
    RED = "\033[31m"
    RESET = "\033[0m"
    
    while True:
        max_index = len(task_manager.get_tasks())
        remove_input = input("Choose one option to remove: ") #TODO create option to get more inputs at once 
        index = validate_user_input(remove_input, max_index, 1, "remove")
        
        if index is not None: # input is valid
            task_to_remove = task_manager.tasks[index - 1]
            confirm = input(f"Press ENTER to {RED}delete{RESET} '{task_to_remove.description}', or any other key to cancel: ")
            if confirm == "":
                removed_task = task_manager.remove_task(index)
                if removed_task is not None:
                    print(f"{task_to_remove.description} was removed!")
                else:
                    print("Unexpected error. Removal cancelled")
            else:
                print("Deletion cancelled")
        else:
            print("Invalid index. No tasks deleted")

def handle_complete(task_manager):
    GREEN = "\033[92m"
    RESET = "\033[0m"
    
    while True: 
        max_index = len(task_manager.get_tasks())
        complete_input = input("Choose one to mark as completed: ") #TODO same as remove_tasks
        index = validate_user_input(complete_input, max_index, 1, "complete")
        if index is not None:
            task_to_complete = task_manager.tasks[index - 1]
            confirm = input(f"Press ENTER to {GREEN}complete{RESET} '{task_to_complete.description}', or any other key to cancel: ")
            if confirm == "":
                completed_task = task_manager.complete_task(index)
                if completed_task is not None:
                    print(f"{task_to_complete.description} completed sucessifuly!!")
                else:
                    print("UnUnexpected error. Action cancelled ")
            else:
                print("Action cancelled")
        else:
            print("Invalid index. No tasks completed")

