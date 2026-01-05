from collections import UserDict
import re

class MyExceptionValueError(Exception):
    pass

class Field: #Базовий клас для полів запису.
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field): #Клас для зберігання імені контакту. Обов'язкове поле.
	pass

# 3. Клас Phone:
#     Реалізовано валідацію номера телефону (має бути перевірка на 10 цифр).
#     Наслідує клас Field. Значення зберігaється в полі value .
class Phone(Field): #Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
    def __init__(self, value):
        match = re.match(r'^\d{10}$', value)
        if match is None:
            raise MyExceptionValueError(f"Invalid phone number format: {value}")
        super().__init__(value)

# 2. Клас Record:
#     Реалізовано зберігання об'єкта Name в атрибуті name.
#     Реалізовано зберігання списку об'єктів Phone в атрибуті phones.
#     Реалізовано метод для додавання - add_phone. На вхід подається рядок, який містить номер телефона.
#     Реалізовано метод для видалення - remove_phone. На вхід подається рядок, який містить номер телефона.
#     Реалізовано метод для редагування - edit_phone. На вхід подається два аргумента - рядки, які містять старий номер телефона та новий. У разі некоректності вхідних даних метод має завершуватись помилкою ValueError.
#     Реалізовано метод для пошуку об'єктів Phone - find_phone. На вхід подається рядок, який містить номер телефона. Метод має повертати або об’єкт Phone, або None .
class Record: #Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number: str):
        phone = Phone(phone_number)
        self.phones.append(phone.value)
    
    def remove_phone(self, phone_number: str):
        try:
            self.phones.remove(str(Phone(phone_number)))
        except:
            raise KeyError("Phone number not found.")
    
    def edit_phone(self, old_phone_number: str, new_phone_number: str):
        phone = Phone(new_phone_number)
        for i, phone in enumerate(self.phones):
            if phone == old_phone_number:
                self.phones[i] = new_phone_number
            
    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone == phone_number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p for p in self.phones)}"

# 1. Клас AddressBook:
#     Має наслідуватись від класу UserDict .
#     Реалізовано метод add_record, який додає запис до self.data. Записи Record у AddressBook зберігаються як значення у словнику. В якості ключів використовується значення Record.name.value.
#     Реалізовано метод find, який знаходить запис за ім'ям. На вхід отримує один аргумент - рядок, якій містить ім’я. Повертає об’єкт Record, або None, якщо запис не знайден.
#     Реалізовано метод delete, який видаляє запис за ім'ям.
#     Реалізовано магічний метод __str__ для красивого виводу об’єкту класу AddressBook .
class AddressBook(UserDict): #Клас для зберігання та управління записами.
    def __init__(self):
        self.data = {}

    def __str__(self):
        result = "Address Book:\n"
        for record in self.data:
            result += f"{self.data.get(record)}" + "\n"
        return result.strip()

    def add_record(self, record: Record):
        self.data[record.name.value] = record
    
    def find(self, name: str):
        return self.data.get(name, None)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

# Функціональність:
#     AddressBook:Додавання записів.
#     Пошук записів за іменем.
#     Видалення записів за іменем.
#     Record:Додавання телефонів.
#     Видалення телефонів.
#     Редагування телефонів.
#     Пошук телефону.

#Після реалізації ваш код має виконуватися наступним чином:
# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
    
print(book)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

# Видалення запису Jane
book.delete("Jane")








