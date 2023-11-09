import pickle
import os

class NoteManager:
    def __init__(self, filename='notes.pkl'):
        self.filename = filename
        self.notes = self.load_notes()

    def add_note(self, note):
        self.notes.append(note)
        self.save_notes()

    def save_notes(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.notes, f)

    def load_notes(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                try:
                    return pickle.load(f)
                except EOFError:  # Handle empty pickle file error
                    return []
        return []

    def show_notes(self):
        if not self.notes:
            print("No notes to show.")
        else:
            for index, note in enumerate(self.notes, start=1):
                print(f"Note {index}: {note}")

    def __str__(self):
        return "\n".join(self.notes)


note_manager = NoteManager()

while True:
    command = input().strip().lower()  # Strip whitespace and convert to lower case for consistency
    if command == 'note':
        note = input("Enter your note: ") 
        note_manager.add_note(note)
        print("Note added.")
    elif command == 'note show':
        note_manager.show_notes()
    elif command == 'exit':
        break
