import sqlite3
from src.database.database_manager import DatabaseManager

class Model:
    TABLE_NAME = ""
    FIELDS_NAMES = ['id']
    def __init__(self, id):
        self.id = id

### GETTERS ###
    def get_id(self):
        return self.id

    @classmethod
    def get_fields_names(cls):
        return FIELDS_NAMES

    def get_values(self):
        return [self.id]

    def get_fields(self):
        return dict(zip(FIELDS_NAMES, self.get_values()))

### DATABASE METHODS ###
    def update(self, fields):
        print(fields)
        DatabaseManager.update(self.TABLE_NAME, self.id, fields)
        return self.select({'id': self.id})

    def delete(self):
        DatabaseManager.delete(self.TABLE_NAME, self.id)

### DATABASE CLASS METHODS ###
    @classmethod
    def insert(cls, fields):
        DatabaseManager.insert(cls.TABLE_NAME, fields)
        return cls.select(fields)

    @classmethod
    def select(cls, where_fields={}, limit=None, offset=None, order_col=None, desc=None):
        return [cls.get_by_row(row) for row in DatabaseManager.select(
            cls.TABLE_NAME, cls.FIELDS_NAMES, where_fields, limit, offset, order_col, desc)]
    
    @classmethod
    def delete_where(cls, fields={}):
        return DatabaseManager.delete_where(cls.TABLE_NAME, fields)

