"""Console bot helper"""

from src.ContactBook.models import ObjectValidateError, AddressBook, Record, Phone, Email, Birthday
from src.tools.common import CommandHandler
from src.View.base_view import ConsoleView
from functools import wraps


def handle_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ObjectValidateError as e:
            return str(e)
        except KeyError:
            return 'Enter user name'
        except ValueError:
            return 'Give me name and phone please'
        except IndexError:
            return 'Invalid command format'
        except PermissionError as e:
            return f'No access rights! {str(e)}'
        except Exception as e:
            return f'An unexpected error occurred: {str(e)}'
    return wrapper


class ContactManager:
    def __init__(self, address_book):
        self.address_book = address_book

    def handle_invalid_command(self, *args):
        return 'Invalid command format'

    def handle_hello(*args):
        return 'How can I help you?'


    def handle_end(*args):
        return 'Good bye!'


    @handle_error
    def handle_contact_add(self, command):
        def input_field(prompt, field_type):
            while True:
                value = input(prompt)
                if not value:
                    return None
                try:
                    return field_type(value)
                except ObjectValidateError as e:
                    print(e)

        name = input_field('Name:', str)

        phones = []
        while True:
            phone = input_field('Phone (10 digits only): ', Phone)
            if phone:
                phones.append(phone.value)
                add_another_phone = input('Do you want to add another phone? (yes/no): ').lower()
                if add_another_phone != 'yes':
                    break

        email = input_field('Email:', Email)
        birthday = input_field('Birthday (dd.mm.yyyy):', Birthday)
        address = input('Address:')

        record = Record(name, birthday=birthday.value if isinstance(birthday, Birthday) else None,
                        email=email.value if isinstance(email, Email) else None,
                        address=address)

        for phone in phones:
            record.add_phone(phone.strip())

        self.address_book.add_record(record)

        phone_numbers = ', '.join(phones) if phones else 'None'
        email_str = f', email: {email.value}' if email else ''
        birthday_str = f', birthday: {birthday.value}' if birthday else ''
        address_str = f', address: {address}' if address else ''

        result = f'Contact {name} added with phone numbers: {phone_numbers}{email_str}{birthday_str}{address_str}'
        return result


    @handle_error
    def handle_delete_contact(self, command):
        name = ' '.join(command)
        record = self.address_book.find(name)

        if not record:
            return f'Contact "{name}" not found'

        self.address_book.delete(name)

        return f'Contact "{name}" deleted successfully'


    @handle_error
    def handle_contact_get_by_name(self, command):
        name = command[0]
        record = self.address_book.find(name)
        if record:
            return str(record)

        return f'Contact {name} not found'


    @handle_error
    def handle_contact_search(self, command):
        query = command[0]
        records = self.address_book.search_full(query)

        if records:
            return f'Founded contacts:\n' + '\n'.join([str(record) for record in records])

        return f'No contacts found for the request "{query}"'

    def handle_congratulate(self, command):
        try:
            days_ahead = int(command[0])
            for record in self.address_book.data.values():
                if record.birthday:
                    result = record.birthday.congratulate(self.address_book, days_ahead)
                    return result
            return "No contacts with birthday information found"
        except (ValueError, IndexError):
            return 'Use "congratulate n" where n is the number of days from the current date.'


    def handle_contact_get_all(self, *args):
        if not self.address_book.data:
            return 'No contacts found'

        result = ''
        for page in self.address_book.iterator():
            for record in page:
                result += f'Name: {record.name.value}\n'
                result += f'Phones: {", ".join(record.get_phones_list())}\n'
                if record.email:
                    result += f'Email: {record.email.value}\n'
                if record.birthday:
                    days_to_birthday = record.days_to_birthday()
                    birthday_info = f'({days_to_birthday} days left)' if days_to_birthday is not None else ''
                    result += f'Birthday: {record.birthday.value}{birthday_info}\n'
                if record.address:
                    result += f'Address: {record.address.value}\n'
                result += '\n'

        return result


class ContactCommandHandler(CommandHandler):
    def __init__(self, manager):
        commands = {
            '1': manager.handle_contact_add,
            '2': manager.handle_delete_contact,
            '3': manager.handle_contact_get_by_name,
            '4': manager.handle_contact_search,
            '5': manager.handle_contact_get_all,
            '6': manager.handle_hello,
            '7': manager.handle_end,
            '8': manager.handle_end
        }
        super().__init__(commands, manager)
        self.manager = manager


def main():
    address_book = AddressBook()
    address_book.load_data_from_file()
    manager = ContactManager(address_book)
    contact_command_handler = ContactCommandHandler(manager)

    while True:
        options = {
            '1': 'Add contact',
            '2': 'Delete contact',
            '3': 'Get contact by name',
            '4': 'Search contacts',
            '5': 'Show all contacts',
            '6': 'Say hello',
            '7': 'Say good bye',
            '8': 'Close'
        }
        choice = input("\n".join([f"{key}. {value}" for key, value in options.items()]) + "\nEnter the n: ").strip()

        if choice == '7':
            print(manager.handle_end())
            break

        result = contact_command_handler.handle_command(choice)

        if result == 'Good bye!':
            print(result)
            break
        else:
            print(result)

    address_book.save_data_to_file()

