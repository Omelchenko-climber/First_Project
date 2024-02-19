from src.ContactManager.models import ObjectValidateError, AddressBook, Record, Name, Phone
from src.tools.common import CommandHandler, handle_error
from src.View.base_view import ConsoleView


def handle_validation_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ObjectValidateError as e:
            print(f"Validation error occurred: {e}")
            return None
        except IOError as e:
            print(f"I/O error occurred: {e}")
            return None
    return wrapper


class ContactManager:
    """Class to manage contacts."""
    def __init__(self, address_book, view):
        """
        Initialize ContactManager.

        :param address_book: The address book containing contacts.
        :param view: The view for displaying messages.
        """
        self.address_book = address_book
        self.view = view

    @handle_error
    @handle_validation_errors
    def handle_add_contact(self):
        """
        Handle the addition of a new contact.
        """
        name = input('Name: ')
        phones_input = input('Phones (comma-separated, 10 digits only): ')
        phones = [phone.strip() for phone in phones_input.split(',')]
        email = input('Email (optional): ')
        birthday = input('Birthday (optional, dd.mm.yyyy): ')
        address = input('Address (optional): ')

        record = Record(name, email=email, birthday=birthday, address=address)
        record.phones.extend(Phone(phone_number) for phone_number in phones)
        self.address_book.add_record(record)
        self.address_book.save_data_to_file()
        self.view.display_message(f'Contact {name} added.')

    @handle_error
    @handle_validation_errors
    def handle_change_contact(self):
        """
        Handle the modification of an existing contact.
        """
        name_to_change = input('Enter the name of the contact to change: ')
        contact = self.address_book.find(name_to_change)

        if contact:
            name = input('Name: ')
            phones_input = input('Phones (comma-separated, 10 digits only): ')
            phones = [phone.strip() for phone in phones_input.split(',')]
            email = input('Email (optional): ')
            birthday = input('Birthday (optional, dd.mm.yyyy): ')
            address = input('Address (optional): ')

            contact.name = Name(name)
            contact.phones = [Phone(phone) for phone in phones]
            if email:
                contact.add_email(email)
            if birthday:
                contact.set_birthday(birthday)
            if address:
                contact.add_address(address)
            self.address_book.save_data_to_file()
            self.view.display_message(f'Contact {name_to_change} changed.')
        else:
            self.view.display_message(f'Contact with name "{name_to_change}" not found.')

    @handle_error
    def handle_delete_contact(self):
        """
        Handle the deletion of a contact.
        """
        name = self.view.get_input("Enter the name of the contact to delete: ")
        if self.address_book.find(name):
            self.address_book.delete(name)
            self.address_book.save_data_to_file()
            self.view.display_message(f"Contact '{name}' successfully deleted.")
        else:
            self.view.display_message(f"Contact with the name '{name}' not found.")

    @handle_error
    def handle_get_contact_by_name(self):
        """
        Handle retrieving contact information by name.
        """
        name = self.view.get_input("Enter the name of the contact to search for: ")
        record = self.address_book.find(name)
        if record:
            self.view.display_message(str(record))
        else:
            self.view.display_message(f"Contact with the name '{name}' not found.")

    @handle_error
    def handle_search_contacts(self):
        """
        Handle searching for contacts based on a query.
        """
        query = self.view.get_input("Enter the query to search for contacts: ")
        found_contacts = self.address_book.search_full(query)
        if found_contacts:
            self.view.display_message("Found contacts:")
            for contact in found_contacts:
                self.view.display_message(str(contact))
        else:
            self.view.display_message(f"No contacts found for the query '{query}'.")

    def handle_display_all_contacts(self):
        """
        Handle displaying all contacts.
        """
        all_contacts = self.address_book.iterator()
        found_contacts = False
        for page in all_contacts:
            for contact in page:
                self.view.display_message(str(contact))
                found_contacts = True
        if not found_contacts:
            self.view.display_message("No contacts found.")

    @handle_error
    def handle_congratulate(self):
        """
        Handles the congratulate command.

        Asks the user to input the number of days for congratulations.
        If a valid number is provided, it congratulates all contacts whose birthdays are within the specified number
         of days.
        If no contacts with birthday information are found, it displays a message accordingly.

        Raises:
            ValueError: If the input provided is not a valid number.
        """
        days = self.view.get_input("Enter the number of days for congratulations: ")
        try:
            days = int(days)
            for record in self.address_book.data.values():
                if record.birthday:
                    result = record.birthday.congratulate(self.address_book, days)
                    self.view.display_message(result)
                    return
            self.view.display_message("No contacts with birthday information found.")
        except ValueError:
            self.view.display_message("Please enter a valid number of days.")


class ContactCommandHandler(CommandHandler):
    """Command handler for contact management."""
    def __init__(self, manager, view):
        """
        Initialize ContactCommandHandler.

        :param manager: The ContactManager instance.
        :param view: The view for displaying messages.
        """
        super().__init__(manager, view)
        commands = {
            '1': ("Add contact", manager.handle_add_contact),
            '2': ("Change contact", manager.handle_change_contact),
            '3': ("Delete contact", manager.handle_delete_contact),
            '4': ("Get contact info", manager.handle_get_contact_by_name),
            '5': ("Search", manager.handle_search_contacts),
            '6': ("Show all contacts", manager.handle_display_all_contacts),
            '7': ("Greets", manager.handle_congratulate),
            '0': ("Return to main menu", self.return_to_main_menu())
        }
        super().__init__(commands, view)
        self.manager = manager

    def handle_command(self, choice):
        """
        Handle the selected command.

        :param choice: User's choice of command.
        """
        command = self.commands.get(choice)
        if command:
            command[1]()
        else:
            self.view.display_message('Invalid choice. Please select a valid option.')

    def return_to_main_menu(self):
        """
        Return to the main menu.
        """
        return


def run_contact_manager():
    """
    Run the contact manager program.
    """

    program_name = "Contact Manager V0.1"
    view = ConsoleView()
    address_book = AddressBook()
    address_book.load_data_from_file()
    manager = ContactManager(address_book, view)
    contact_command_handler = ContactCommandHandler(manager, view)

    while True:
        options = {
            '1': 'Add contact',
            '2': 'Change contact',
            '3': 'Delete contact',
            '4': 'Get contact by name',
            '5': 'Search contacts',
            '6': 'Show all contacts',
            '7': 'Congratulate',
            '0': 'Return to Main Menu'
        }
        choice = view.display_menu(program_name, options)
        if choice in ['1', '2', '3', '4', '5', '6', '7']:
            contact_command_handler.handle_command(choice)
        elif choice == '0':
            return
        else:
            view.display_message('Invalid choice. Please select a valid option.')


if __name__ == '__main__':
    run_contact_manager()
