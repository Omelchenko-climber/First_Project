from abc import ABC, abstractmethod


class BaseView(ABC):
    @abstractmethod
    def display_message(self, message):
        """
        Отображает сообщение пользователю.
        """
        pass

    @abstractmethod
    def get_input(self, prompt):
        """
        Запрашивает ввод от пользователя с подсказкой.
        """
        pass

    @abstractmethod
    def display_program_name(self, program_name):
        pass

    @abstractmethod
    def display_menu(self, program_name, options):
        """
        Отображает меню с опциями.
        """
        pass

    @abstractmethod
    def get_confirmation(self, message):
        """
        Запрашивает у пользователя подтверждение (да/нет).
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
        for key, value in options.items():
            print(f'{key}. {value}')
        choice = input('Choose option: ')
        return choice

    def get_confirmation(self, message):
        response = input(f'{message} (yes/no): ')
        return response.lower() in ['yes']


