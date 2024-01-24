import sqlite3
from src.database.database_manager import DatabaseManager
from .model import Model

class PhysicalDVDModel(Model):
    TABLE_NAME = 'physical_dvd'
    FIELDS_NAMES = ['id', 'physical_code', 'dvd_id', 'rental_state']
    def __init__(self, id, physical_code, dvd_id, rental_state):
        super().__init__(id)
        self.physical_code = physical_code
        self.dvd_id = dvd_id
        self.rental_state = rental_state
    
### GETTERS ###
    def get_physical_code(self):
        return self.physical_code

    def get_dvd_id(self):
        return self.dvd_id
    
    def get_email(self):
        return self.email

    def get_rental_state(self):
        return self.rental_state

    def get_values(self):
        return [self.id, self.physical_code, self.dvd_id, self.rental_state]

    @classmethod
    def get_by_row(cls, row):
        return PhysicalDVDModel(row[0], row[1], row[2], row[3])

