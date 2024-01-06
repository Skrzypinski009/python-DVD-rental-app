import sqlite3
from src.database.database_manager import DatabaseManager

class DVDModel:
    fields_names = ['id', 'name', 'date']
    def __init__(self, id, name, date):
        self.id = id
        self.name = name
        self.date = date
    
### GETTERS ###
    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_date(self):
        return self.date

### SETTERS ###
    def set_id(self, id):
        self.id = id

    def set_name(self, name):
        self.name = name

    def set_date(self, date):
        self.date = date

### DATABASE METHODS ###
    def update(self):
        DatabaseManager.update('dvd', [self.id, self.name, self.date], self.fields_names)

    def delete(self):
        DatabaseManager.delete('dvd', self.id)

### DATABASE CLASS METHODS ###
    @classmethod
    def insert(cls, name, date):
        DatabaseManager.insert('dvd', [name,date], cls.fields_names[1:])

    @classmethod
    def select(cls, id=None, name=None, date=None, limit=None, offset=None):
        return DatabaseManager.select("dvd", [id,name,date], cls.fields_names, limit, offset)
    
    @classmethod
    def delete_where(cls, id=None, name=None, date=None):
        return DatabaseManager.delete_where('dvd', [id,name,date], cls.fields_names)

### OTHER ###
    @classmethod
    def get_by_row(cls, row):
        return DVDModel(row[0], row[1], row[2])



