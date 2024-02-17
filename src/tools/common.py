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
