from todoist_api_python.api import TodoistAPI
import sys
from datetime import datetime, timedelta


api = TodoistAPI("755a8992983b0540febf3a6c66c4d9c16a7b9d31")


# MENUS


def display_menu():
    """
    Menu to navigate program functions
    """
    print("\nTodoCLI:")
    print("1. Show tasks")
    print("2. Create tasks")
    print("3. Complete task")
    print("4. Exit program")


def user_choice(user_choice):
    """
    Sub-menus depending on user choice from menu
    """
    if user_choice == 1:
        print("\nWhich tasks do you want to view?")
        print("1. Overdue")
        print("2. Today")
        print("3. Weekly")
        print("4. Return to previous menu")
    elif user_choice == 2:
        print("Create task")
        create_task()
        return_to_menu()

    elif user_choice == 3:
        complete_task()
        return_to_menu()

    elif user_choice == 4:
        print("Exiting program...")
        sys.exit()


def return_to_menu():
    """
    Restarts main() function to give the impression that the user
    is sent back to main menu
    """
    print("\nPress Enter to go back to the menu...")
    input("\n")
    print("----------------------------------------")
    main()


def return_to_tasks_menu():
    """
    Restarts main() function to give the impression that the user
    is sent back to main menu
    """
    print("\nPress Enter to return to the tasks menu...")
    input("\n")
    print("----------------------------------------")
    user_input = 1
    user_choice(user_input)
    user_input = get_user_input()
    view_tasks(user_input)

# USER INPUT RESPONSE


def get_user_input():
    """
    Record user input and return it if valid
    """
    while True:
        try:
            choice = int(input("Enter your choice: "))
            print("----------------------------------------")
            if 1 <= choice <= 4:
                return choice
            else:
                print("Please enter a valid choice.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def view_tasks(user_choice):
    """
    Sub-menu if user choose to view tasks
    """
    if user_choice == 1:
        get_overdue_tasks()
        return_to_tasks_menu()
    elif user_choice == 2:
        get_todays_tasks()
        return_to_tasks_menu()
    elif user_choice == 3:
        get_weekly_tasks()
        return_to_tasks_menu()
    elif user_choice == 4:
        main()


# API FUNCTIONS

# Get tasks from api


def get_todays_tasks():
    """
    Get tasks market with the "Today" tag from todoist
    """
    try:
        tasks = api.get_tasks(
            filter='today'
        )

        if not tasks:
            print("\nAll tasks completed for today.")
            return

    except Exception as error:
        print(error)

    print("\nTasks due today:")
    print("----------")
    for id, task in enumerate(tasks, start=1):
        task_name = task.content
        due_date = task.due.date
        print(f"{id}. {task_name} - {due_date}")
    print("----------")


def get_overdue_tasks():
    """
    Get tasks marked with the today or overdue filter tag
    """
    try:
        tasks = api.get_tasks(
            filter='overdue'
        )

        if not tasks:
            print("\nNo overdue tasks.")
            return

    except Exception as error:
        print(error)
    print("\nOverdue tasks:")
    print("----------")
    for id, task in enumerate(tasks, start=1):
        task_name = task.content
        due_date = task.due.date
        print(f"{id}. {task_name} - {due_date}")
    print("----------")


def get_weekly_tasks():
    """
    Get tasks due before next monday
    """
    try:
        tasks = api.get_tasks(
            filter='due before: mon'
        )

        if not tasks:
            print("\nAll tasks completed for the week.")
            return

    except Exception as error:
        print(error)

    print("\nTasks due this week:")
    print("----------")
    for id, task in enumerate(tasks, start=1):
        task_name = task.content
        due_date = task.due.date
        task_id = task.id
        print(f"{id}. {task_name} - {due_date}")
    print("----------")

    """
    Returning tasks list so the complete_task function can call it
    """
    return tasks


# Create tasks


def create_task():
    """
    Create tasks with name and due date
    """
    print("----------")
    task_name = input("Enter task: ")
    while True:
        task_due = input("Enter task due date (e.g., tomorrow, 2025-01-01): ")
        try:
            due_date = validate_due_date(task_due)
            break
        except ValueError as ve:
            print(f"Error: {ve}")
            print("Please enter a valid due date.")

    try:
        task = api.add_task(
            content=str(task_name),
            due_string=str(task_due),
        )

    except Exception as error:
        print(error)

    created_name = task.content
    created_due_date = task.due.date
    print("\nSuccessfully created task:")
    print("----------")
    print(f"Task name: {created_name}")
    print(f"With due date: {created_due_date}")

# Task due date validation


def validate_due_date(input_due_date):
    """
    Parse and validate the input due date
    """
    today = datetime.today()

    if input_due_date.lower() == 'today':
        return today.strftime('%Y-%m-%d')

    if input_due_date.lower() == 'tomorrow':
        return (today + timedelta(days=1)).strftime('%Y-%m-%d')

    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                'saturday', 'sunday']
    lower_input = input_due_date.lower()

    if lower_input in weekdays:
        days_until_next_weekday = (today.weekday() - weekdays.ind(
        lower_input)) % 7
        due_date = today + timedelta(days=days_until_next_weekday)
        return due_date.strftime('%Y-%m-%d')

    return datetime.strptime(input_due_date, '%Y-%m-%d').strftime('%Y-%m-%d')

# Complete task


def complete_task():
    """
    Gets tasks list from weekly tasks function and completes
    the selected task with task id
    """
    try:
        tasks = get_weekly_tasks()

        if not tasks:
            return

        selected_task_number = int(input(
            "\nEnter the number of the task you want to complete: "))

        if 1 <= selected_task_number <= len(tasks):
            selected_task = tasks[selected_task_number - 1]
            task_name = selected_task.content
            task_date = selected_task.due.date
            task_id = selected_task.id
            is_success = api.close_task(task_id=task_id)
            print(f"\nSuccessfully completed task:")
            print("----------")
            print(f"{task_name} - {task_date}")
            print("----------")
        else:
            print("Invalid task number. Please enter a valid number.")
    except Exception as error:
        print(error)

# MAIN


def main():
    display_menu()
    user_input = get_user_input()
    user_choice(user_input)
    user_input = get_user_input()
    view_tasks(user_input)


main()
