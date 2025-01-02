import csv
import os

class DataController:
    def __init__(self, file, fields):
        self.file = file
        self.fields = fields
        self.key = fields[0]

        if not os.path.exists(self.file):
            with open(self.file, mode='w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.fields)
                writer.writeheader()

    def read(self):
        with open(self.file, mode='r', newline='') as file:
            return csv.DictReader(file, fieldnames=self.fields)
    
    def read_all(self):
        with open(self.file, mode='r', newline='') as file:
            return list(csv.DictReader(file, fieldnames=self.fields))
    
    def find(self, value):
        for entry in self.read():
            if entry[self.key] == value:
                return entry
        return None

    def add(self, *args):
        if self.find(args[0]):
            return False
        
        with open(self.file, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writerow(dict(zip(self.fields, args)))
        return True
    
    def remove(self, value):
        entry_to_remove = self.find(value)
        if not entry_to_remove:
            return None
        
        entries = self.read_all()
        with open(self.file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writeheader()
            for entry in entries:
                if entry[self.key] != value:
                    writer.writerow(entry)
        return entry_to_remove