import datetime
from .task import Task
from .task_manager import TaskManager
from v2 import task
from wcwidth import wcswidth
from v2 import task_manager

def pad_cell(text, width):
    visual_width = wcswidth(text)
    pad = width - visual_width
    left = pad // 2
    right = pad - left
    return " " * left + text + " " * right

# Valide user input          
def validate_user_input(user_input, max_index, min_index, context):
    while True:
        try:
            if user_input == "":
                return
            user_input = int(user_input)

            if not (min_index <= user_input <= max_index):
                print(f"Invalid option. Please only enter a number between {min_index} and {max_index}.")
                retry = input("Press ENTER to go back or type another option: ")
                if retry == "":
                    return
                user_input = retry
                continue

        except ValueError:
            print(f"Invalid input. Please enter a valid number between {min_index} and {max_index}.")
            retry = input("Press ENTER to go back or type another option: ")
            if retry == "":
                return
            user_input = retry
            continue

        return user_input

        
# Display a list of options and return the chosen one
def show_options(prompt, question, options):
    if prompt is not None:
        print(prompt)
    for idx, opt in enumerate(options, 1):
        print(f"{idx}. {opt}")
    #while True:
    choice = input(question)
    return choice
        
# Validate user input for menu options
def show_main_menu(task_manager):
       
    while True:
        to_do_list = task_manager.get_tasks()
        option = show_options("----------- Menu -----------", "Choose one: ",["View Tasks", "Add Task", "Complete Task", "Remove Task", "Exit"])
        valid_option = validate_user_input(option, 5, 1, "show_main_menu")
        if valid_option == 1:
            print_task_table(task_manager.get_tasks())

            option = show_options(None,"Choose one:  ",["Add task","Complete Task", "Remove Task", "Go back"])
            valid_option = validate_user_input(option, 4, 1, "after_view_list")
            if valid_option == 1:
                handle_add(task_manager)
            elif valid_option == 2:
                handle_complete(task_manager)
            elif valid_option == 3:
                handle_remove(task_manager)
            elif valid_option == 4:
                show_main_menu(task_manager)

        elif valid_option == 2:
            handle_add(task_manager)
        elif valid_option == 3:
            print_task_table(task_manager.get_tasks())
            handle_complete(task_manager)
        elif valid_option == 4:
            print_task_table(task_manager.get_tasks())
            handle_remove(task_manager) 
        elif valid_option == 5:
            handle_exit(task_manager)

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

def handle_post_view_options(task_manager):
    option = show_options(None,"Choose one:  ",["Add task","Complete Task", "Remove Task", "Go back"])
    valid_option = validate_user_input(option, 4, 1, "after_view_list")
    if valid_option == 1:
        handle_add(task_manager)
    elif valid_option == 2:
        handle_complete(task_manager)
    elif valid_option == 3:
        handle_remove(task_manager)
    elif valid_option == 4:
        show_main_menu(task_manager)                                     


def handle_add(task_manager):
    """
    Handles adding a new task.
    Permite múltiplas tentativas caso a tarefa já exista e oferece opções ao usuário ao final.
    Sai ao pressionar ENTER em qualquer input de task.
    """
    while True:
        # 1. Peça a descrição da tarefa
        new_task = input("Enter a task: ").strip()
        if new_task == "":
            # Usuário apertou ENTER para sair
            return

        # 2. Checa duplicidade (enquanto a tarefa já existir)
        while any(t.description.lower().strip() == new_task.lower() for t in task_manager.get_tasks()):
            print("This task is already on the list.")
            retry = input("Press ENTER to go back or type a new task: ").strip()
            if retry == "":
                return  # Usuário desistiu, volta ao menu
            new_task = retry  # Tenta novamente com o novo valor

        # 3. Agora temos uma task nova!
        try:
            task = Task(new_task, False, datetime.datetime.now())
            task_manager.add_task(task)
            task_manager.save_to_file("tasks.json")
            print(f"Task '{new_task}' added!")
        except Exception as e:
            print(f"Error while adding the task: {e}")
            return  # Se deu erro inesperado, retorna para o menu principal

        # 4. Oferece as opções pós-adicionar
        while True:
            option = show_options(None, "What next? ", ["Add another", "View list", "Back to main menu"])
            valid_option = validate_user_input(option, 3, 1, "after_add_task")

            if valid_option == 1:
                # Volta para o começo do loop externo para adicionar outra
                break
            elif valid_option == 2:
                # Mostra a tabela e chama o menu de ações pós-view
                print_task_table(task_manager.get_tasks())
                handle_post_view_options(task_manager)
                return  # Depois de ver lista, volta ao menu principal
            elif valid_option == 3:
                # Volta ao menu principal
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

                    option = show_options(None, "What Next? ",["Remove another", "View list", "Back to main menu"])
                    valid_option = validate_user_input(option, 3, 1, "after_remove_task")

                    if valid_option == 1:
                        continue
                    elif valid_option == 2:
                        print_task_table(task_manager.get_tasks())
                        handle_post_view_options(task_manager)
                    elif valid_option == 3:
                        return

                else:
                    print("Unexpected error. Removal cancelled")
            else:
                print("Deletion cancelled")
        else:
            print("Invalid index. No tasks deleted")

def handle_complete(task_manager): #TODO conferir se a task ja esta completada
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
                    task_manager.save_to_file("tasks.json")
                    
                    option = show_options(None, "What Next? ",["Complete another", "View list", "Back to main menu"])
                    valid_option = validate_user_input(option, 3, 1, "after_remove_task")

                    if valid_option == 1:
                        continue

                    elif valid_option == 2:
                        print_task_table(task_manager.get_tasks())
                        handle_post_view_options(task_manager)
                    elif valid_option == 3:
                        return
                    
                else:
                    print("UnUnexpected error. Action cancelled ")
            else:
                print("Action cancelled")
        else:
            print("Invalid index. No tasks completed")

def handle_exit(task_manager):
    if task_manager.get_tasks():          
        save_tasks = input("Do you want to keep your tasks saved? (yes/no)").strip().lower()
        while True:    
            if save_tasks.startswith("y"):
                try:
                    task_manager.save_to_file("tasks.json")
                    print(f"{len(task_manager.get_tasks())} tasks were saved to 'tasks.json'")
                    
                except Exception as e:
                    print("Error while saving tasks.")
                print("Thanks for using my terminal app. See you next time!") 
                exit()
            
            if save_tasks.startswith("n"):
                try: 
                    task_manager.tasks = []  # esvazia a lista de tarefas
                    task_manager.save_to_file("tasks.json")  # salva a lista vazia no arquivo
                    print("All tasks deleted!")
                except Exception as e:
                    print("Error while deleting tasks.")
                print("Thanks for using my terminal app. See you next time!") 
                exit()

            else:
                save_tasks = input("Invalid input. Type (yes/no) or press ENTER to exit program: ")
                if save_tasks == "":
                    print("Thanks for using my terminal app. See you next time!")  
                    exit()  
                else:
                    continue  
    else: 
        print("Thanks for using my terminal app. See you next time!")    
        exit()


            
