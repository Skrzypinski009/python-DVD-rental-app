import sqlite3
from src.database.database_manager import DatabaseManager
from .model import Model

class DVDCategoryRelationModel(Model):
    TABLE_NAME = 'dvd_category_relation'
    FIELDS_NAMES = ['id', 'dvd_id', 'category_id']
    def __init__(self, id, dvd_id, category_id):
        super().__init__(id)
        self.dvd_id = dvd_id
        self.category_id = category_id
    
### GETTERS ###
    def get_dvd_id(self):
        return self.dvd_id

    def get_category_id(self):
        return self.category_id

    def get_values(self):
        return [self.id, self.dvd_id, self.category_id]

    @classmethod
    def get_by_row(cls, row):
        return DVDCategoryRelationModel(row[0], row[1], row[2])

