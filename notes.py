import pickle
import os

class Note:
    def __init__(self, filename='notes.pkl'):
        self.filename = filename
        self.notes = self.load_notes()

    def add(self, note):
        self.notes.append(note)
        self.save()

    def save(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.notes, f)

    def load_notes(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                try:
                    return pickle.load(f)
                except EOFError:
                    return []
        return []

    def show(self):
        if not self.notes:
            print("No notes to show.")
        else:
            for index, note in enumerate(self.notes, start=1):
                print(f"Note {index}: {note}")

    def search(self, query):
        matches = [note for note in self.notes if query.lower() in note.lower()]
        if not matches:
            print("No matches found.")
        else:
            for index, note in enumerate(matches, start=1):
                print(f"Match {index}: {note}")

note = Note()

while True:
    command = input(">>>").strip().lower()
    if command == 'note':
        note_text = input("Enter your note: ") 
        note.add(note_text)
        print("Note added.")
    elif command == 'note show':
        note.show()
    elif command == 'search':
        query = input("Enter search query: ")
        note.search(query)
    elif command == 'exit':
        break
