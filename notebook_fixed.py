from typing import List
import json
from tabulate import tabulate

class Note:
    def __init__(self, id, text):
        self.id = id
        self.text = text

    def __str__(self):
        return f"ID: {self.id}\nContent: {self.text}"

class Notebook:
    def __init__(self, notes: List[Note] = None):
        if notes is not None:
            self.notes = notes
        else:
            self.notes = []

    def add_note(self, note: Note):
        self.notes.append(note)
        self.import_to_file("For_notebook.json")  
        print("Your note added successfully")

    def update_note(self, note_id: int, new_text: str):
        for note in self.notes:
            if note.id == note_id:
                note.text = new_text
                self.import_to_file("For_notebook.json")  
                print(f"The note with ID {note_id} updated")
                return
        print(f"The note with ID {note_id} is not present in this notebook")

    def remove_note(self, note_id: int):
        for i, note in enumerate(self.notes):
            if note.id == note_id:
                del self.notes[i]
                self.import_to_file("For_notebook.json")  
                print(f"The note with ID {note_id} was removed")
                return
        print("The note with the id you entered is not present")

    def list_notes(self):
        column_name = ["ID", "NOTE"]
        tabulated_table = [[note.id, note.text] for note in self.notes]
        print(tabulate(tabulated_table, headers=column_name))

    def demonstrate_notes(self, note_id: int):
        for note in self.notes:
            if note.id == note_id:
                print(note)
                return
        print(f"The note with ID {note_id} is not present")

    def import_to_file(self, file: str):
        with open(file, "w") as f:
            json.dump([note.__dict__ for note in self.notes], f)
        print(f"All notes were saved to {file}")

    def import_from_file(self, file: str):
        try:
            with open(file, 'r') as f:
                notes = json.load(f)
                self.notes = [Note(**note) for note in notes]
            print(f"Notes were imported from {file}.")
        except FileNotFoundError:
            print(f"{file} not found.")

class ConsoleApp:
    def __init__(self):
        self.noting = Notebook()
        self.file = 'For_notebook.json'
        self.noting.import_from_file(self.file)

    def add_note(self):
        content = input("Enter the note you want to add: ")
        note_id = len(self.noting.notes) + 1
        self.noting.add_note(Note(note_id, content))

    def update_note(self):
        note_id = int(input("Enter note ID to update: "))
        new_content = input("Enter the new note: ")
        self.noting.update_note(note_id, new_content)

    def remove_note(self):
        note_id = int(input("Enter the ID you want to delete: "))
        self.noting.remove_note(note_id)

    def list_notes(self):
        self.noting.list_notes()

    def show_note_details(self):
        note_id = int(input("Enter the id of your note: "))
        self.noting.demonstrate_notes(note_id)

    def save_and_quit(self):
        self.noting.import_to_file(self.file)

    def Menu(self):
        while True:
            print("\nNotebook Menu:")
            print("1: Show All Notes")
            print("2: Show Note Details")
            print("3: Create Note")
            print("4: Update Note")
            print("5: Delete Note")
            print("Q: Save and Quit")
            print("M: Show Menu Again")

            button = input("Enter your button: ").upper()

            if button == "1":
                self.list_notes()
            elif button == "2":
                self.show_note_details()
            elif button == "3":
                self.add_note()
            elif button == "4":
                self.update_note()
            elif button == "5":
                self.remove_note()
            elif button == "Q":
                self.save_and_quit()
                break
            elif button == "M":
                print("\nReturning to the menu...")
            else:
                print("There is no this kind of button.")

if __name__ == "__main__":
    Application = ConsoleApp()
    Application.Menu()
