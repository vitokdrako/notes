from Address_book import AddressBook, Record, DuplicatedPhoneError, Note


records = None
note = Note()


def input_error(*expected_args):
    def input_error_wrapper(func):
        def inner(*args):
            try:
                return func(*args)
            except IndexError:
                return f"Please enter {' and '.join(expected_args)}"
            except KeyError:
                return f"The record for contact {args[0]} not found. Try another contact or use help."
            except ValueError as error:
                if error.args:
                    return error.args[0]
                return f"Phone format '{args[1]}' is incorrect. Use digits only for phone number."
            except DuplicatedPhoneError as phone_error:
                return f"Phone number {phone_error.args[1]} already exists for contact {phone_error.args[0]}."
            except AttributeError:
                return f"Contact {args[0]} doesn't have birthday yet."
        return inner
    return input_error_wrapper

def capitalize_user_name(func):
    def inner(*args):
        new_args = list(args)
        new_args[0] = new_args[0].capitalize()
        return func(*new_args)
    return inner

def unknown_handler(*args):
    return f"Unknown command. Use <help>"

def help_handler():
    help_txt = ""
    def inner(*args):
        nonlocal help_txt
        if not help_txt:
            with open("help.txt") as file:            
                help_txt = "".join(file.readlines())
        return help_txt
    return inner

@capitalize_user_name
@input_error("name", "phone")
def add_handler(*args):
    user_name = args[0]
    user_phones = args[1:]
    record = records.find(user_name, True)
    if not record:
        record = Record(user_name)
        for user_phone in user_phones:
            record.add_phone(user_phone)
        records.add_record(record)
        return f"New record added for {user_name} with phone number{'s' if len(user_phones) > 1 else ''}: {'; '.join(user_phones)}."
    else:
        response = []
        for user_phone in user_phones:
            record.add_phone(user_phone)
            response.append(f"New phone number {user_phone} for contact {user_name} added.")
        return "\n".join(response)

@capitalize_user_name
@input_error("name", "old_phone", "new_phone")
def change_handler(*args):
    user_name = args[0]
    old_phone = args[1]
    new_phone = args[2]
    record = records.find(user_name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"Phone number for {user_name} changed from {old_phone} to {new_phone}."

@capitalize_user_name    
@input_error("name")
def birthday_handler(*args):
    user_name = args[0]
    user_birthday = args[1] if len(args) > 1 else None
    record = records.find(user_name)
    if record:
        if user_birthday:
            record.add_birthday(user_birthday)
            return f"Birthday {user_birthday} for contact {user_name} added."
        else:
            return f"{record.days_to_birthday()} days to the next {user_name}'s birthday ({record.birthday})."

@capitalize_user_name    
@input_error("name")
def delete_handler(*args):
    user_name = args[0]
    user_phones = args[1:]
    if len(user_phones) >= 1:
        record = records.find(user_name)
        if record:
            response = []
            for user_phone in user_phones:
                record.remove_phone(user_phone)
                response.append(f"Phone number {user_phone} for contact {user_name} removed.")
            return "\n".join(response)
    else:
        if records.delete(user_name):
            return f"Record for contact {user_name} deleted."
        return f"Record for contact {user_name} not found."


@input_error([])
def greeting_handler(*args):
    greeting = "How can I help you?"
    return greeting

@capitalize_user_name
@input_error("name")
def phone_handler(*args):
    user_name = args[0]
    record = records.find(user_name)
    if record:
        return "; ".join(p.value for p in record.phones)

@input_error("term")
def search_handler(*args):
    term: str = args[0]
    contacts = records.search_contacts(term)
    if contacts:
        return "\n".join(str(contact) for contact in contacts)
    return f"No contacts found for '{term}'."

@input_error([])
def show_all_handler(*args):
    return records.iterator()

@input_error("note text")
def note_add_handler(*args):
    note_text = " ".join(args)
    note.add(note_text)
    return "Note added."

@input_error("search query")
def note_search_handler(*args):
    search_query = " ".join(args)
    search_results = note.search(search_query)
    if search_results:
        return "\n".join(search_results)
    return "No notes found."

def note_show_handler(*args):
    return str(note)

COMMANDS = {
            help_handler(): "help",
            greeting_handler: "hello",
            add_handler: "add",
            change_handler: "change",
            phone_handler: "phone",
            search_handler: "search",
            birthday_handler: "birthday",
            show_all_handler: "show all",
            delete_handler: "delete",
            note_add_handler: "note add", 
            note_show_handler: "note show",
            note_search_handler: "note search"
        }
EXIT_COMMANDS = {"good bye", "close", "exit", "stop", "g"}

def parser(text: str):
    for func, kw in COMMANDS.items():
        if text == kw: 
            return func, []
        elif text.startswith(kw + " "): 
            return func, text[len(kw):].strip().split()
    return unknown_handler, []

def main():
    global records, note
    with AddressBook("address_book.pkl") as book:
        records = book
        note = Note()
        while True:
            user_input = input(">>> ").lower()
            if user_input in EXIT_COMMANDS:
                print("Good bye!")
                break
            
            func, data = parser(user_input)
            result = func(*data)
            if isinstance(result, str):
                print(result)
            else:
                for i in result:                
                    print ("\n".join(i))
                    input("Press enter to show more records")


if __name__ == "__main__":
    main()