from datetime import datetime, timedelta
from collections import UserDict
from itertools import islice
import os
import pickle
import re


class ObjectValidateError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Field:
    def __init__(self, value):
        valid, msg = self.is_valid(value)
        if not valid:
            raise ObjectValidateError(msg)
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        valid, msg = self.is_valid(value)
        if not valid:
            raise ObjectValidateError(msg)
        self.__value = value

    def is_valid(self, new_value):
        return True, None

    def __eq__(self, other):
        return self.__value == other

    def __ne__(self, other):
        return self.__value == other

    def __str__(self):
        return str(self.__value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        super().__init__(phone)

    def is_valid(self, phone):
        if not phone.isdigit() or len(phone) != 10:
            return False, f'Invalid phone number "{phone}"! Must be contain 10 digits only'
        return True, None


class Email(Field):
    def __init__(self, email):
        super().__init__(email)

    def is_valid(self, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False, f'Invalid email address "{email}"'
        return True, None


class Birthday(Field):
    def __init__(self, birthday):
        super().__init__(birthday)

    def is_valid(self, birthday):
        try:
            datetime.strptime(birthday, "%d.%m.%Y")
        except ValueError:
            return False, f'Invalid birthday "{birthday}". Right birthday forman dd.mm.yyyy'
        else:
            return True, None

    @classmethod
    def congratulate(cls, address_book, days_ahead):
        current_date = datetime.now()
        future_date = current_date + timedelta(days=days_ahead)

        congratulation_list = []

        for record in address_book.data.values():
            days_to_birthday = record.days_to_birthday()
            if days_to_birthday is not None and days_to_birthday == days_ahead:
                congratulation_list.append(record)

        if congratulation_list:
            result = f'Congratulations to the following contacts, whose birthday is in {days_ahead} days:\n'
            for record in congratulation_list:
                result += f'{record.name.value} - Birthday: {record.birthday.value}\n'
        else:
            result = f'No contacts have birthdays in {days_ahead} days'

        return result


class Address(Field):
    def __init__(self, address):
        super().__init__(address)

    def is_valid(self, address):

        return True, None


class Record:
    def __init__(self, name, birthday=None, email=None, address=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None
        self.email = Email(email) if email else None
        self.address = Address(address) if address else None

    def add_phone(self, phone):
        if phone not in self.get_phones_list():
            new_phone = Phone(phone)
            self.phones.append(new_phone)

    def remove_phone(self, phone):
        phone_index = self.get_phones_list().index(phone)
        del self.phones[phone_index]

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, desired_phone_number):
        for phone in self.phones:
            if phone.value == desired_phone_number:
                return phone

    def get_phones_list(self) -> list:
        return [phone.value for phone in self.phones]

    def add_email(self, email):
        if not self.email:
            self.email = Email(email)
        else:
            raise ObjectValidateError('Email already exist for this contact')

    def remove_email(self):
        self.email = None

    def add_address(self, address):
        if not self.address:
            self.address = Address(address)
        else:
            raise ObjectValidateError('Address already exist for this contact')

    def remove_address(self):
        self.address = None

    def set_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if not self.birthday:
            return
        birthday = datetime.strptime(self.birthday.value, "%d.%m.%Y")
        now = datetime.now()
        next_birthday = datetime(now.year, birthday.month, birthday.day)
        if next_birthday < now:
            next_birthday = datetime(now.year + 1, birthday.month, birthday.day)
        return (next_birthday - now).days

    def __str__(self):
        text_view = f"Contact name: {self.name.value}; phones: {', '.join(p.value for p in self.phones)}"
        if self.email:
            text_view += f'; email: {self.email.value}' if self.email else ''
        text_view += '; days to birthday: ' + str(self.days_to_birthday()) if self.birthday else ''
        if self.address:
            text_view += f'; address: {self.address.value}' if self.address else ''

        return text_view


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

        self.data_file_name = 'address_book.bin'
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.data_file_path = os.path.join(self.current_directory, self.data_file_name)

    def save_data_to_file(self):
        if not os.access(self.current_directory, os.W_OK):
            raise PermissionError(f"Cannot write to: {self.data_file_path}")

        file_path = os.path.join(self.current_directory, self.data_file_name)
        with open(file_path, 'wb') as file:
            pickle.dump(self.data, file)

    def load_data_from_file(self):
        # check for file exists and read access rights
        if os.path.exists(self.data_file_path) and os.access(self.current_directory, os.R_OK):
            with open(self.data_file_path, 'rb') as file:
                # check loading data
                loaded_data = pickle.load(file)
                for name, record in loaded_data.items():
                    if isinstance(record, Record) and self.validate_record(record):
                        self.add_record(record)
                    else:
                        # if at least one error is found, then return an empty AddressBook.
                        self.data = {}
                        return
        else:
            self.data = {}

    @staticmethod
    def validate_record(record):
        if not isinstance(record.name, Name):
            return False
        for phone in record.phones:
            if not isinstance(phone, Phone):
                return False
        if record.birthday:
            if not isinstance(record.birthday, Birthday):
                return False
        return True

    def add_record(self, record):
        if record.name.value in self.data:
            raise ObjectValidateError(f'Contact with name {record.name.value} already exist. Try with another one')
        self.data[record.name.value] = record

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find(self, name):
        return self.data.get(name, None)

    def search_full(self, query):
        found_records = []
        query = query.lower().strip()

        for record in self.data.values():
            if query in record.name.value.lower() or query in ' '.join(record.get_phones_list()):
                found_records.append(record)

        return found_records

    def iterator(self, page_size=10):
        keys = list(self.data.keys())
        for i in range(0, len(keys), page_size):
            yield [self.data[key] for key in islice(keys, i, i + page_size)]
