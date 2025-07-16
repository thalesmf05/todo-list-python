import json
import os

# Save the task list to a JSON file
def save_tasks(to_do_list):
    with open("tasks.json", "w") as file:
        json.dump(to_do_list, file)

# Load the task list from a JSON file
def load_tasks():
    if os.path.exists("tasks.json"):
        try:
            with open("tasks.json", "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Failed to load tasks. File is corrupted.")
            return []
    return []

# Pause execution so user can read messages
def pause():
    input("Press ENTER to continue...")

# Print all tasks with status icons
def show_to_do_list(to_do_list):
    if not to_do_list:
        print("No tasks added yet.")
        pause()
        return False
    print("-------- To-Do List --------")
    for index, task in enumerate(to_do_list, start=1):
        status = "✅" if task["completed"] else "❌"
        print(f"{index}. {task['task']} - {status}")
    return True

# Check if the task already exists in the list
def task_already_added(to_do_list, new_task):
    for task in to_do_list:
        if task["task"].lower().strip() == new_task.lower().strip():
            return True
    return False

# Validate user input for menu options
def user_input_validation(user_input, max_value, min_value):
    try:
        user_input = int(user_input)
        if not (min_value <= user_input <= max_value):
            print("Invalid option. Please try again.")
            return None
    except ValueError:
        print("Invalid option. Please try again.")
        return None
    else:
        return user_input

# Display a list of options and return the chosen one
def show_options(prompt, options):
    print(prompt)
    for idx, opt in enumerate(options, 1):
        print(f"{idx}. {opt}")
    while True:
        choice = input("Choose one: ")
        validated = user_input_validation(choice, len(options), 1)
        if validated is not None:
            return validated

# Flow to add a new task to the list
def add_task_flow(to_do_list):
    while True:
        new_task = input("Enter a task: ")
        if task_already_added(to_do_list, new_task):
            print("This task is already on the list!")
            continue
        dic_task = {"task": new_task.strip(), "completed": False}
        to_do_list.append(dic_task)
        save_tasks(to_do_list)
        print("Task added!")
        option = show_options("What next?", ["Add another", "View list", "Back to main menu"])
        if option == 1:
            continue
        elif option == 2:
            view_list(to_do_list)
        elif option == 3:
            break


# Flow to mark a task as completed
def mark_task_completed(to_do_list):
    while True:
        if not show_to_do_list(to_do_list):
            return
        mark_complete_input = input("Choose a task number to mark as completed: ")
        mark_complete = user_input_validation(mark_complete_input, len(to_do_list), 1)
        if mark_complete is not None:
            to_do_list[mark_complete - 1]["completed"] = True
            save_tasks(to_do_list)
            print("Task marked as completed!")
            option = show_options("What next?", ["Mark another", "View list", "Back to main menu"])
            if option == 1:
                continue
            elif option == 2:
                view_list(to_do_list)
            elif option == 3:
                show_main_menu()

# Flow to remove a task from the list
def remove_task(to_do_list):
    while True:
        if not show_to_do_list(to_do_list):
            return
        remove_option_input = input("Choose a task number to remove: ")
        remove_option = user_input_validation(remove_option_input, len(to_do_list), 1)
        if remove_option is not None:
            confirm = input(f"Are you sure you want to remove '{to_do_list[remove_option - 1]['task']}'? (yes/no): ").strip().lower()
            if confirm == "yes":
                del to_do_list[remove_option - 1]
                save_tasks(to_do_list)
                print("Task removed!")
            else:
                print("Removal cancelled.")
            if to_do_list:
                option = show_options("What next?", ["Remove another task", "View list", "Back to main menu"])
                if option == 1:
                    continue
                elif option == 2:
                    view_list(to_do_list)
                elif option == 3:
                    show_main_menu()
            else:
                print("No more tasks. Going back to main menu.")
                break

# View task list and choose what to do with tasks
def view_list(to_do_list):
    if not show_to_do_list(to_do_list):
        return
    while True:
        option = show_options("Modify Tasks:", ["Mark task as completed", "Remove task", "Back to main menu"])
        if option == 1:
            mark_task_completed(to_do_list)
        elif option == 2:
            remove_task(to_do_list)
        elif option == 3:
            show_main_menu()

# Display the main menu and control the app flow
def show_main_menu():
    while True:
        to_do_list = load_tasks()

        option = show_options("----------- Menu -----------", ["View Tasks", "Add Task", "Exit"])
        if option == 1:
           view_list(to_do_list)
           continue
        elif option == 2:
            add_task_flow(to_do_list)
        elif option == 3:
            print("Exiting program. Thank you!")
            exit()


# Start the program
if __name__ == "__main__":
    show_main_menu()



