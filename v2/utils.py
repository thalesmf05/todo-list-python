import datetime
from task import Task
from task_manager import TaskManager
from wcwidth import wcswidth 
import os 
#TODO depois de deletar todas as tasks bug 
# Path to the JSON file where tasks are stored.
json_path = os.path.join(os.path.dirname(__file__), "tasks.json")

def pad_cell(text, width):
    """
    Centers text within a given width using spaces. Useful for aligning table columns.
    """
    visual_width = wcswidth(text)
    pad = width - visual_width
    left = pad // 2
    right = pad - left
    return " " * left + text + " " * right

def validate_single_input(user_input, max_index, min_index):
    """Convert the input to an integer and ensure it is within bounds."""

    try:
        value = int(user_input)
        if not (min_index <= value <= max_index):
            return None
    except ValueError:
        return None

    return value
           
def get_valid_single_input(max_index, min_index):
    """Prompt the user for a single valid option within the given range."""

    user_entry = None

    while True:
        if user_entry is None:
            user_entry = input("Choose one option: ").strip()

        if user_entry == "":
            print("You must enter something!")
            user_entry = None
            continue

        index = validate_single_input(user_entry, max_index, min_index)
        if index is not None:
            return index
        else:
            print(f"Invalid input. Please enter a number between {min_index}-{max_index}")
            retry = input("Press ENTER to go back or type another option: ").strip()
            if retry == "":
                return None
            user_entry = retry


def get_multiple_inputs(task_manager):
    """Collect and validate multiple comma-separated options."""

    valid_inputs = []
    invalid_inputs = []
    while True:
        raw_input = input("Choose one or more options, separated by commas: ").strip()

        if not raw_input:
            print("You must enter something!")
            continue

        options = raw_input.split(",")
        max_index = len(task_manager.get_tasks())

        for option in options:
            index = validate_single_input(option.strip(), max_index, 1)

            if index is not None:
                valid_inputs.append(index)
            else:
                invalid_inputs.append(option.strip())

        break

    return valid_inputs, invalid_inputs

    

def show_options(prompt, options):
    """
    Displays a list of numbered options and prompts user for selection.
    Returns the raw user input (to be validated later).
    """
    if prompt is not None:
        print(prompt)
    for idx, opt in enumerate(options, 1):
        print(f"{idx}. {opt}")
    return

def show_main_menu(task_manager):
    """
    Main navigation menu for the app.
    Loops until the user chooses to exit, showing all main options.
    Delegates actions to other handler functions.
    """
    while True:
        to_do_list = task_manager.get_tasks()
        option = show_options("----------- Menu -----------",["View Tasks", "Add Task", "Complete Task", "Remove Task", "Exit"])
        valid_index = get_valid_single_input(5, 1)
        if valid_index == 1:
            print_task_table(task_manager.get_tasks())
            handle_post_view_options(task_manager)
        elif valid_index == 2:
            handle_add(task_manager)
        elif valid_index == 3:
            print_task_table(task_manager.get_tasks())
            handle_complete(task_manager)
        elif valid_index == 4:
            print_task_table(task_manager.get_tasks())
            handle_remove(task_manager) 
        elif valid_index == 5:
            handle_exit(task_manager)

def print_task_table(tasks):
    """
    Pretty-prints the list of tasks in a formatted table.
    Shows: Number, Task description, Status, Created at, and Deadline (if present).
    Uses pad_cell() for column alignment.
    """
    col_widths = [4, 19, 8, 21, 10]  # No, Task, Status, Created at, Deadline
    table_width = sum(col_widths) + len(col_widths) + 1

    title = "TO-DO LIST MANAGER"
    print("\n" + title.center(table_width))

    print("+" + "+".join("-" * w for w in col_widths) + "+")

    headers = ["No", "Task", "Status", "Created at", "Deadline"]
    header_cells = [pad_cell(h, w) for h, w in zip(headers, col_widths)]
    print("|" + "|".join(header_cells) + "|")

    print("+" + "+".join("-" * w for w in col_widths) + "+")

    if not tasks:
        empty = "No tasks found."
        print("|" + pad_cell(empty, table_width - 2) + "|")
    else:
        for idx, task in enumerate(tasks, 1):
            status = "❌" if not task.completed else "✅"
            created = task.time.strftime("%Y-%m-%d %H:%M")
            # 'deadline' is optional for future extensibility
            deadline = getattr(task, "deadline", "---") or "---"
            cells = [
                pad_cell(str(idx), col_widths[0]),
                pad_cell(task.description[:col_widths[1]], col_widths[1]),
                pad_cell(status, col_widths[2]),
                pad_cell(created, col_widths[3]),
                pad_cell(str(deadline), col_widths[4])
            ]
            print("|" + "|".join(cells) + "|")
    print("+" + "+".join("-" * w for w in col_widths) + "+")

def print_task_text_table(tasks, title):
    """Prints a simplified table showing only task descriptions.

    This is used when the app needs to display a subset of tasks to the
    user, for example, when confirming multiple removals or completions.
    It keeps the same visual style as ``print_task_table`` but only shows
    the task text.
    """
    # Determine column widths dynamically so longer task names fit nicely
    max_task_width = max((wcswidth(t.description) for t in tasks), default=len("Task"))
    col_widths = [4, max(max_task_width, len("Task"))]
    table_width = sum(col_widths) + len(col_widths) + 1

    print("\n" + title.center(table_width))
    print("+" + "+".join("-" * w for w in col_widths) + "+")

    headers = ["No", "Task"]
    header_cells = [pad_cell(h, w) for h, w in zip(headers, col_widths)]
    print("|" + "|".join(header_cells) + "|")

    print("+" + "+".join("-" * w for w in col_widths) + "+")

    if not tasks:
        empty = "No tasks found."
        print("|" + pad_cell(empty, table_width - 2) + "|")
    else:
        for idx, task in enumerate(tasks, 1):
            cells = [
                pad_cell(str(idx), col_widths[0]),
                pad_cell(task.description, col_widths[1]),
            ]
            print("|" + "|".join(cells) + "|")

    print("+" + "+".join("-" * w for w in col_widths) + "+")

def handle_post_view_options(task_manager):
    """
    Presents post-list options to the user after viewing the table.
    """
    option = show_options(None,["Add task","Complete Task", "Remove Task", "Go back"])
    valid_index = get_valid_single_input(4, 1)
    if valid_index == 1:
        handle_add(task_manager)
    elif valid_index == 2:
        handle_complete(task_manager)
    elif valid_index == 3:
        handle_remove(task_manager)
    elif valid_index == 4:
        show_main_menu(task_manager)                                     

def handle_add(task_manager):
    """
    Handles the process of adding a new task.
    Checks for duplicates and allows the user to add multiple tasks in sequence.
    Saves to disk after each addition.
    """
    while True:
        new_task = input("Enter a task: ").strip()
        if new_task == "":
            # User pressed ENTER to exit
            return

        # Prevents adding duplicate tasks (case insensitive, whitespace ignored)
        while any(t.description.lower().strip() == new_task.lower() for t in task_manager.get_tasks()):
            print("This task is already on the list.")
            retry = input("Press ENTER to go back or type a new task: ").strip()
            if retry == "":
                return
            new_task = retry

        try:
            task = Task(new_task, False, datetime.datetime.now())
            task_manager.add_task(task)
            task_manager.save_to_file(json_path)
            print(f"Task '{new_task}' added!")
        except Exception as e:
            print(f"Error while adding the task: {e}")
            return

        while True:
            option = show_options(None, ["Add another", "View list", "Back to main menu"])
            valid_index = get_valid_single_input(3, 1)

            if valid_index == 1:
                break  # Start loop again to add another
            elif valid_index == 2:
                print_task_table(task_manager.get_tasks())
                handle_post_view_options(task_manager)
                return
            elif valid_index == 3:
                return

def handle_remove(task_manager):
    """
    Handles removing tasks from the list.
    Confirms removal and offers next steps after each removal.
    """
    while True:
        if not task_manager.get_tasks():
            print("No tasks to remove.")
            return
        valid_inputs, invalid_inputs = get_multiple_inputs(task_manager)
        valid_inputs = sorted(set(valid_inputs))
        invalid_inputs = sorted(set(invalid_inputs))

        if valid_inputs:
            selected_tasks = [task_manager.tasks[i - 1] for i in valid_inputs]
            print_task_text_table(selected_tasks, "TASKS TO REMOVE")

            confirm = input("Press ENTER to delete tasks or type any key to cancel: ")
            if confirm == "":
                for idx in sorted(valid_inputs, reverse=True):
                    task_manager.remove_task(idx)
                task_manager.save_to_file(json_path)
                print(f"Tasks {', '.join(str(i) for i in valid_inputs)} were deleted.")
            else:
                print("Action cancelled")
        else:
            print("No valid tasks selected.")

        if invalid_inputs:
            print(f"Invalid inputs: {', '.join(invalid_inputs)}")

        option = show_options(None, ["Remove more", "View list", "Back to main menu"])
        valid_index = get_valid_single_input(3, 1)

        if valid_index == 1:
            continue
        elif valid_index == 2:
            print_task_table(task_manager.get_tasks())
            handle_post_view_options(task_manager)
            return
        elif valid_index == 3:
            return


def handle_complete(task_manager):
    """
    Handles marking tasks as completed.
    Confirms completion and saves the update to disk.
    """
    GREEN = "\033[92m"
    RESET = "\033[0m"

    while True:
        if not task_manager.get_tasks():
            print("No tasks to complete.")
            return
        valid_inputs, invalid_inputs = get_multiple_inputs(task_manager)
        valid_inputs = sorted(set(valid_inputs))
        invalid_inputs = sorted(set(invalid_inputs))

        if valid_inputs:
            selected_tasks = [task_manager.tasks[i - 1] for i in valid_inputs]
            print_task_text_table(selected_tasks, "TASKS TO COMPLETE")

            confirm = input(f"Press ENTER to {GREEN}complete{RESET} tasks or type any key to cancel: ")
            if confirm == "":
                already_done = []
                completed_now = []
                for idx in valid_inputs:
                    task = task_manager.tasks[idx - 1]
                    if task.completed:
                        already_done.append(str(idx))
                        continue
                    completed_task = task_manager.complete_task(idx)
                    if completed_task is not None:
                        completed_now.append(str(idx))
                task_manager.save_to_file(json_path)
                if already_done:
                    print(f"Tasks {', '.join(already_done)} already completed.")
                if completed_now:
                    print(f"{GREEN}Tasks {', '.join(completed_now)} completed!{RESET}")
            else:
                print("Action cancelled")
        else:
            print("No valid tasks selected.")

        if invalid_inputs:
            print(f"Invalid inputs: {', '.join(invalid_inputs)}")

        option = show_options(None, ["Complete more", "View list", "Back to main menu"])
        valid_index = get_valid_single_input(3, 1)

        if valid_index == 1:
            continue
        elif valid_index == 2:
            print_task_table(task_manager.get_tasks())
            handle_post_view_options(task_manager)
            return
        elif valid_index == 3:
            return

def handle_exit(task_manager):
    """
    Handles application exit.
    Prompts the user to save or delete tasks before quitting the program.
    Ensures persistent storage is updated on exit.
    """
    if task_manager.get_tasks():          
        save_tasks = input("Do you want to keep your tasks saved? (yes/no)").strip().lower()
        while True:    
            if save_tasks.startswith("y"):
                try:
                    task_manager.save_to_file(json_path)
                    print(f"{len(task_manager.get_tasks())} tasks were saved to 'tasks.json'")
                    
                except Exception as e:
                    print("Error while saving tasks.")
                print("Thanks for using my terminal app. See you next time!") 
                exit()
            
            if save_tasks.startswith("n"):
                try: 
                    task_manager.tasks = []  # clears the task list
                    task_manager.save_to_file(json_path)  # saves the empty list
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



            
