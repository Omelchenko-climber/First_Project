from src.NoteManger.note_manager import NoteManager, NoteCommandHandler, run_note_manager
from src.EventManager.event_manager import EventManager, EventCommandHandler, run_event_manager
from src.View.base_view import ConsoleView


def main():
    view = ConsoleView()

    while True:
        options = {
            '1': 'Note Manager',
            '2': 'Event Manager',
            '0': 'Exit'
        }
        choice = view.display_menu(options)

        if choice == '1':
            run_note_manager()
        elif choice == '2':
            run_event_manager()
        elif choice == '0':
            exit()
        else:
            view.display_message('Invalid choice. Please select a valid option.')


if __name__ == '__main__':
    main()
