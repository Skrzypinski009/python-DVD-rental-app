import sqlite3
from datebase.database_manager import DatabaseManager

class DVDModel:
    fields_names = ['id', 'name', 'date']
    def __init__(id, name, date):
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
        DatabaseManager.update('dvd', [self.id, self.name, self.date], fields_names)

    def delete(self):
        DatabaseManager.delete('dvd', self.id)

### DATABASE CLASS METHODS ###
    @classmethod
    def select(cls, id=None, name=None, date=None):
        return DatabaseManager.select("dvd", [id,name,date], fields_names)
    
    @classmethod
    def delete_where(cls, id=None, name=None, date=None):
        return DatabaseManager.delete_where('dvd', [id,name,date], fields_names)



