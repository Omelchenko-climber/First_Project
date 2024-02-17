from src.View.base_view import ConsoleView
from src.ContactBook.contact_manager import ContactCommandHandler
from src.NoteJournal.note_manager import NoteManager, NoteCommandHandler, EventManager, EventCommandHandler
from src.tools.common import handle_error, CommandHandler


class NestedMenuCommandHandler(CommandHandler):
    def __init__(self, address_book, note_file_path, event_file_path, view):
        self.address_book = address_book
        self.note_file_path = note_file_path
        self.event_file_path = event_file_path
        super().__init__(self.get_commands(), view)

    def get_commands(self):
        commands = {
            "1": self.handle_contact_menu,
            "2": self.handle_note_menu,
            "3": self.handle_event_menu,
            "0": exit
        }
        return commands

    def handle_contact_menu(self):
        contact_handler = ContactCommandHandler(self.address_book, self.view)
        while True:
            contact_options = {
                '1': 'Add contact',
                '2': 'Change contact',
                '3': 'Delete contact',
                '4': 'Get contact by name',
                '5': 'Search contact',
                '6': 'Set birthday',
                '7': 'Congratulate',
                '8': 'Get all contacts',
                '0': 'Exit nested menu'
            }
            choice = self.view.display_menu(contact_options)
            if choice == '0':
                break
            result = contact_handler.handle_command(choice)
            self.view.display_message(result)

    def handle_note_menu(self):
        note_manager = NoteManager(self.note_file_path, self.view)
        note_handler = NoteCommandHandler(note_manager, self.view)
        while True:
            note_options = {
                '1': 'Add note',
                '2': 'Search note',
                '3': 'Edit note',
                '4': 'Delete note',
                '5': 'Add tag to note',
                '6': 'Show all notes',
                '0': 'Exit nested menu'
            }
            choice = self.view.display_menu(note_options)
            if choice == '0':
                break
            result = note_handler.handle_command(choice)
            self.view.display_message(result)

    def handle_event_menu(self):
        event_manager = EventManager(self.event_file_path, self.view)
        event_handler = EventCommandHandler(event_manager, self.view)
        while True:
            event_options = {
                '1': 'Add event',
                '2': 'Show upcoming events',
                '3': 'Show all events',
                '0': 'Exit nested menu'
            }
            choice = self.view.display_menu(event_options)
            if choice == '0':
                break
            result = event_handler.handle_command(choice)
            self.view.display_message(result)


