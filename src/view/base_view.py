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
    def display_menu(self, options):
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

    def display_menu(self, options):
        for key, value in options.items():
            print(f"{key}. {value}")
        choice = input("Выберите опцию: ")
        return choice

    def get_confirmation(self, message):
        response = input(f"{message} (да/нет): ")
        return response.lower() in ['да', 'yes']


