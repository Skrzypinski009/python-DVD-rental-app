import sqlite3
from src.database.database_manager import DatabaseManager
from .model import Model

class CategoryModel(Model):
    TABLE_NAME = 'category'
    FIELDS_NAMES = ['id', 'name']
    def __init__(self, id, name):
        super().__init__(id)
        self.name = name
    
### GETTERS ###
    def get_name(self):
        return self.name

    def get_values(self):
        return [self.id, self.name]

    @classmethod
    def get_by_row(cls, row):
        return CategoryModel(row[0], row[1])
