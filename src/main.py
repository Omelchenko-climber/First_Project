from src.ContactManager.contact_manager import run_contact_manager
from src.NoteManger.note_manager import run_note_manager
from src.EventManager.event_manager import run_event_manager
from src.FileManager.file_sorter import run_file_sorter, counter
from src.View.base_view import ConsoleView


def main():
    view = ConsoleView()

    while True:
        program_name = "Main Menu"
        options = {
            '1': 'Contact Manager',
            '2': 'Note Manager',
            '3': 'Event Manager',
            '4': 'File Manager',
            '0': 'Exit'
        }
        choice = view.display_menu(program_name, options)

        if choice == '1':
            run_contact_manager()
        elif choice == '2':
            run_note_manager()
        elif choice == '3':
            run_event_manager()
        elif choice == '4':
            file_manager_menu(view)
        elif choice == '0':
            exit()
        else:
            view.display_message('Invalid choice. Please select a valid option.')


def file_manager_menu(view):
    while True:
        program_name = "File Manager V0.1"
        options = {
            '1': 'Sort Files',
            '0': 'Return to Main Menu'
        }
        choice = view.display_menu(program_name, options)

        if choice == '1':
            run_file_sorter()
            counter()
        elif choice == '0':
            return
        else:
            view.display_message('Invalid choice. Please select a valid option.')


if __name__ == '__main__':
    main()
