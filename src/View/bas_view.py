from abc import ABC, abstractmethod
from tabulate import tabulate


class BaseView(ABC):
    @abstractmethod
    def display_message(self, message):
        """
        Displays a message to the user.
        """
        pass

    @abstractmethod
    def get_input(self, prompt):
        """
        Requests input from the user with a prompt.
        """
        pass

    @abstractmethod
    def display_program_name(self, program_name):
        """
        Displays the name of the program.
        """
        pass

    @abstractmethod
    def display_menu(self, program_name, options):
        """
        Displays a menu with options.
        """
        pass

    @abstractmethod
    def get_confirmation(self, message):
        """
        Requests confirmation from the user (yes/no).
        """
        pass


class ConsoleView(BaseView):
    def display_message(self, message):
        print(message)

    def get_input(self, prompt):
        return input(prompt)

    def display_program_name(self, program_name):
        print(f"\n== {program_name} ==")

    def display_menu(self, program_name, options):
        self.display_program_name(program_name)
        print(tabulate(options.items(), tablefmt="presto"))
        choice = input('Choose option: ')
        return choice

    def get_confirmation(self, message):
        response = input(f'{message} (yes/no): ')
        return response.lower() in ['yes']
