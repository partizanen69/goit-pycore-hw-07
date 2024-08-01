from collections import UserDict

class Field:
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return str(self.value)

class Name(Field):
  pass

class Phone(Field):
  def __init__(self, value: str):
    if not value.isdigit() or len(value) != 10:
      raise ValueError(f'Phone must be a number of length 10') 
    super().__init__(value)

class Record:
  def __init__(self, name: str) -> None:
    self.name = Name(name)
    self.phones = []

  def add_phone(self, phone: str) -> None:
    phone = phone.strip()
    found = False
    try:
      self.find_phone(phone)
      found = True  
    except:
      pass

    if found:
       raise ValueError(f'Phone {phone} already exists in contacts')
    
    self.phones.append(Phone(phone))

  def remove_phone(self, phone: str) -> None:
    phone = phone.strip()
    self.phones = list(filter(lambda p: p['value'] == phone, self.phones))
    print(f'Phone {phone} successfully removed')
  
  def edit_phone(self, old_phone: str, new_phone: str) -> None:
    found_phone = self.find_phone(old_phone.strip())
    found_phone.value = new_phone
    print(f'New phone {new_phone} successfully replaced old phone {old_phone}')
  
  def find_phone(self, phone: str) -> str:
    phone = phone.strip()
    
    found_phone = next((p for p in self.phones if p.value == phone), None)
    if found_phone == None:
      raise Exception(f'Phone {phone} not found in contacts')
    
    return found_phone

  def __str__(self):
    return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"



class AddressBook(UserDict):
  def __init__(self):
    super().__init__()
    self.last_id = 0

  def add_record(self, record: Record) -> None:
    self.last_id += 1
    self.data[self.last_id] = record

  def find(self, name: str) -> tuple[str, Record] | None:
    record = next((record for record in self.data.values() if record.name.value == name), None)
    return record
  
  def delete(self, name: str):
    key = next((key for key in self.data.keys() if self.data[key].name.value == name), None)
    if not key:
       raise ValueError(f'record with name {name} not found in contacts')
    del self.data[key]



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
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")
