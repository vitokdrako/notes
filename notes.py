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
                return pickle.load(f)
        return []

    def __str__(self):
        return "\n".join(self.notes)


note_manager = NoteManager()

while True:
    command = input()
    if command == 'note':
        note = input("Enter your note: ") 
        note_manager.add_note(note)
        print("Note added.")
    elif command == 'exit':
        break 