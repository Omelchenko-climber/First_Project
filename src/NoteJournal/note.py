from src.View.base_view import ConsoleView
import json
from functools import wraps


def handle_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'Some error'
        except ValueError:
            return 'Some error'
        except IndexError:
            return 'Some error'
        except PermissionError as e:
            return f'No access rights! {str(e)}'
        except Exception as e:
            return f'An unexpected error occurred: {str(e)}'
    return wrapper


class CommandHandler:
    def __init__(self, commands, view):
        self.commands = commands
        self.view = view

    def handle_command(self, choice):
        if choice in self.commands:
            self.commands[choice]()
        else:
            self.view.display_message('Invalid command')


class Note:
    def __init__(self, title, content, tags):
        self.title = title
        self.tags = tags
        self.content = content

    def __str__(self):
        return f'Title: {self.title}\nTags: {", ".join(self.tags)}\nContent: {self.content}\n'


class NoteManager:
    def __init__(self, file_path, view):
        self.file_path = file_path
        self.notes = self.load_notes()
        self.view = view

    def load_notes(self):
        try:
            with open(self.file_path, 'r') as file:
                notes_data = json.load(file)
                notes = [Note(**note_data) for note_data in notes_data]
                return notes
        except FileNotFoundError:
            return []

    def save_notes(self):
        notes_data = [note.__dict__ for note in self.notes]
        with open(self.file_path, 'w') as file:
            json.dump(notes_data, file, indent=4)

    @handle_error
    def add_note(self):
        title = self.view.get_input('Enter note title: ')
        content = self.view.get_input('Enter note content: ')
        tags = self.view.get_input('Enter tags separated by commas: ').split(',')
        note = Note(title, content, tags)
        self.notes.append(note)
        self.save_notes()
        self.view.display_message('Note added successfully.')

    @handle_error
    def search_note(self):
        query = self.view.get_input('Enter search query: ')
        results = [note for note in self.notes if query in note.title or query in note.content or query in note.tags]
        if results:
            sorted_results = sorted(results, key=lambda note: note.title)
            self.view.display_message('Search results:')
            for note in sorted_results:
                self.view.display_message(str(note))
        else:
            self.view.display_message('No notes found matching the query.')

    @handle_error
    def edit_note(self):
        title = self.view.get_input('Enter the title of the note you want to edit: ')
        new_content = self.view.get_input('Enter the new content for the note: ')
        for note in self.notes:
            if note.title == title:
                note.content = new_content
                self.save_notes()
                self.view.display_message('Note successfully edited.')
                return
        self.view.display_message('Note not found.')

    @handle_error
    def delete_note(self):
        title = self.view.get_input('Enter the title of the note you want to delete: ')
        for note in self.notes:
            if note.title == title:
                self.notes.remove(note)
                self.save_notes()
                self.view.display_message('Note successfully deleted.')
                return
        self.view.display_message('Note not found.')

    @handle_error
    def add_tag_to_note(self):
        title = self.view.get_input('Enter the title of the note to which you want to add a tag: ')
        tag = self.view.get_input('Enter the tag: ')
        for note in self.notes:
            if note.title == title:
                note.tags.append(tag)
                self.save_notes()
                self.view.display_message('Tag successfully added to the note.')
                return
        self.view.display_message('Note not found.')

    @handle_error
    def show_all_notes(self):
        if not self.notes:
            self.view.display_message('No notes found.')
            return
        sorted_notes = sorted(self.notes, key=lambda note: note.title)
        self.view.display_message('All notes:')
        for note in sorted_notes:
            self.view.display_message(str(note))


class NoteCommandHandler(CommandHandler):
    def __init__(self, manager, view):
        commands = {
            "1": manager.add_note,
            "2": manager.search_note,
            "3": manager.edit_note,
            "4": manager.delete_note,
            "5": manager.add_tag_to_note,
            "6": manager.show_all_notes,
            "0": exit
        }
        super().__init__(commands, view)
        self.manager = manager


def main():
    file_path = 'notes.json'
    view = ConsoleView()
    manager = NoteManager(file_path, view)
    note_command_handler = NoteCommandHandler(manager, view)

    while True:
        options = {
            '1': 'Add note',
            '2': 'Search note',
            '3': 'Edit note',
            '4': 'Delete note',
            '5': 'Add tag to note',
            '6': 'Show all notes',
            '0': 'Exit'
        }
        choice = view.display_menu(options)
        note_command_handler.handle_command(choice)


if __name__ == '__main__':
    main()
