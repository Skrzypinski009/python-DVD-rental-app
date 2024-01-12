import sqlite3
from src.database.database_manager import DatabaseManager
from .model import Model

class HistoryLogModel(Model):
    TABLE_NAME = 'history_log'
    FIELDS_NAMES = ['id', 'time_date', 'physical_dvd_id', 'rental_state_id', 'client_id']
    def __init__(self, id, time_date, physical_dvd_id, rental_state_id, client_id ):
        super().__init__(id)
        self.time_date = time_date
        self.physical_dvd_id = physical_dvd_id
        self.rental_state_id = rental_state_id
        self.client_id = client_id
    
### GETTERS ###
    def get_time_date(self):
        return self.time_date

    def get_physical_dvd_id(self):
        return self.physical_dvd_id
    
    def get_rental_state_id(self):
        return self.rental_state_id

    def get_client_id(self):
        return self.client_id

    def get_values(self):
        return [self.id, self.time_date, self.physical_dvd_id, self.rental_state_id, self.client_id]

    @classmethod
    def get_by_row(cls, row):
        return HistoryLogModel(row[0], row[1], row[2], row[3], row[4])