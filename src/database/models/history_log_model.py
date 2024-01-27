from .model import Model

class HistoryLogModel(Model):
    TABLE_NAME = 'history_log'
    FIELDS_NAMES = ['id', 'time_date', 'physical_dvd_id', 'rental_state', 'client_id']
    def __init__(self, id, time_date, physical_dvd_id, rental_state, client_id ):
        super().__init__(id)
        self.__time_date = time_date
        self.__physical_dvd_id = physical_dvd_id
        self.__rental_state = rental_state
        self.__client_id = client_id
    
### GETTERS ###
    def get_time_date(self):
        return self.__time_date

    def get_physical_dvd_id(self):
        return self.__physical_dvd_id
    
    def get_rental_state(self):
        return self.__rental_state

    def get_client_id(self):
        return self.__client_id

    def get_values(self):
        return [self.__id, self.__time_date, self.__physical_dvd_id, self.__rental_state, self.__client_id]

    @classmethod
    def get_by_row(cls, row):
        return HistoryLogModel(row[0], row[1], row[2], row[3], row[4])

