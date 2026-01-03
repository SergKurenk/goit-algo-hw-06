from collections import UserDict
import re

class Field: #Базовий клас для полів запису.
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field): #Клас для зберігання імені контакту. Обов'язкове поле.
    # реалізація класу
		pass

# 3. Клас Phone:
#     Реалізовано валідацію номера телефону (має бути перевірка на 10 цифр).
#     Наслідує клас Field. Значення зберігaється в полі value .
class Phone(Field): #Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
    #super().__init__(value)
    # match = re.match(r'^\+?\d{7,15}$', self.value)
   
    # if match is None:
    #     raise ValueError("Invalid phone number format.")
    # return self.value
    pass

# 2. Клас Record:
#     Реалізовано зберігання об'єкта Name в атрибуті name.
#     Реалізовано зберігання списку об'єктів Phone в атрибуті phones.
#     Реалізовано метод для додавання - add_phone .На вхід подається рядок, який містить номер телефона.
#     Реалізовано метод для видалення - remove_phone. На вхід подається рядок, який містить номер телефона.
#     Реалізовано метод для редагування - edit_phone. На вхід подається два аргумента - рядки, які містять старий номер телефона та новий. У разі некоректності вхідних даних метод має завершуватись помилкою ValueError.
#     Реалізовано метод для пошуку об'єктів Phone - find_phone. На вхід подається рядок, який містить номер телефона. Метод має повертати або об’єкт Phone, або None .
class Record: #Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number: str):
        if Phone(phone_number):
            self.phones.append(phone_number)
        else:
            raise ValueError("Invalid phone number format.")
    
    def remove_phone(self, phone_number: str):
        try:
            self.phones.remove(Phone(phone_number))
        except:
            return "Phone number not found."
    
    def edit_phone(self, old_phone_number: str, new_phone_number: str):
        phone = Phone(new_phone_number)
        if not phone:
            raise ValueError("New phone number is invalid.")
        
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone_number:
                self.phones[i] = new_phone_number
                return
            
    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    # реалізація класу
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

# 1. Клас AddressBook:
#     Має наслідуватись від класу UserDict .
#     Реалізовано метод add_record, який додає запис до self.data. Записи Record у AddressBook зберігаються як значення у словнику. В якості ключів використовується значення Record.name.value.
#     Реалізовано метод find, який знаходить запис за ім'ям. На вхід отримує один аргумент - рядок, якій містить ім’я. Повертає об’єкт Record, або None, якщо запис не знайден.
#     Реалізовано метод delete, який видаляє запис за ім'ям.
#     Реалізовано магічний метод __str__ для красивого виводу об’єкту класу AddressBook .
class AddressBook(UserDict): #Клас для зберігання та управління записами.
    def __init__(self):
        super().__init__()
        self.data = {}

    def __str__(self):
        result = "Address Book:\n"
        for record in self.data.values():
            result += str(record) + "\n"
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










def input_error_decorator(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Контакт не знайдено. Будь ласка, перевірте правильність введеного імені."
        except IndexError:
            return "Недостатньо параметрів для виконання команди. Будь ласка, додайте необхідні аргументи."
        except ValueError:
            return "Недостатньо значень для виконання команди. Додайте будь ласка Ім'я та номер телефону."
    return inner

def parse_input(user_input: str):
    if user_input.strip() == "":
        return "", []
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def show_contacts(contacts:dict[str, str]):
    if len(contacts) == 0:
        return "Список контактів порожній."
    result = "Контакти:\n"
    for name, phone in contacts.items():
        result += f"{name}: {phone}\n"
    return(result.strip())

def check_phone(phone: str) -> bool:
    match = re.match(r'^\+?\d{7,15}$', phone)
    return match is not None

@input_error_decorator 
def change_contact(contacts:dict[str, str], *param) -> str:
    name, phone = param
    if name in contacts:
        if check_phone(phone):
            contacts[name] = phone
            return("Контакт оновлено.")
        else:
            return("Невірний формат номера телефону.")
    else:
        return("Контакт не знайдено.")

@input_error_decorator
def add_contact(contacts:dict[str, str], *param) -> str:
    name, phone = param
    contacts[name] = phone
    return("Контакт додано.")

@input_error_decorator
def del_contact(contacts:dict[str, str], *param) -> str:
    name = param[0]
    # if name in contacts:
    del contacts[name]
    return("Контакт видалено.")
    # else:
        # return("Контакт не знайдено.") 

@input_error_decorator
def show_phone(contacts:dict[str, str], *param) -> str:
    name = param[0]
    return contacts.get(name, "Контакт не знайдено.")

def main():
    cmd = ""
    contacts = {}
    print('Welcome to the assistant bot!')
    while True:
        cmd, *param = parse_input(input("Ведіть команду: "))

        match cmd:
            case "exit":
                print("Бувай!")
                break
            case "add":
                print(add_contact(contacts, *param))
            case "change":
                print(change_contact(contacts, *param))
            case "phone":
                print(show_phone(contacts, *param))
            case 'all':
                print(show_contacts(contacts))
            case 'del':
                print(del_contact(contacts, *param))
            case "hello":
                print("Чим я можу вам допомогти?")
            case "help":
                print("Список всіх команд:")
                print("hello - привітання")
                print("add <ім'я> <номер телефону> - додати новий контакт")
                print("change <ім'я> <номер телефону> - змінити існуючий контакт")
                print("phone <ім'я> - показати номер телефону контакта")
                print("all - показати всі контакти")
                print("del <ім'я> - видалити контакт")
                print("exit - закрити чат")
            case "":
                print("Будь ласка, введіть команду. Для списку команд введіть 'help'.")
            case _:
                print("Вибачте, я не знаю таку команду.")

if __name__ == "__main__":
    main()

