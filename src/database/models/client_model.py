import sqlite3
from src.database.database_manager import DatabaseManager
from .model import Model

class ClientModel(Model):
    TABLE_NAME = 'client'
    FIELDS_NAMES = ['id', 'first_name', 'last_name', 'email', 'phone_number']
    def __init__(self, id, first_name, last_name, email, phone_number):
        super().__init__(id)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
    
### GETTERS ###
    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name
    
    def get_email(self):
        return self.email

    def get_phone_number(self):
        return self.phone_number

    def get_values(self):
        return [self.id, self.first_name, self.last_name, self.email, self.phone_number]

    @classmethod
    def get_by_row(cls, row):
        return ClientModel(row[0], row[1], row[2], row[3], row[4])