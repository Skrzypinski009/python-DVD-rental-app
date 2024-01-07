import sqlite3
from src.database.database_manager import DatabaseManager
from .model import Model

class DVDModel(Model):
    TABLE_NAME = 'dvd'
    FIELDS_NAMES = ['id', 'name', 'date']
    def __init__(self, id, name, date):
        super().__init__(id)
        self.name = name
        self.date = date
    
### GETTERS ###
    def get_name(self):
        return self.name

    def get_date(self):
        return self.date

    def get_values(self):
        return [self.id, self.name, self.date]

    @classmethod
    def get_by_row(cls, row):
        return DVDModel(row[0], row[1], row[2])
