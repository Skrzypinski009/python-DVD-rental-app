from .model import Model

class PhysicalDVDModel(Model):
    TABLE_NAME = 'physical_dvd'
    FIELDS_NAMES = ['id', 'physical_code', 'dvd_id', 'rental_state']
    def __init__(self, id, physical_code, dvd_id, rental_state):
        super().__init__(id)
        self.__physical_code = physical_code
        self.__dvd_id = dvd_id
        self.__rental_state = rental_state
    
### GETTERS ###
    def get_physical_code(self):
        return self.__physical_code

    def get_dvd_id(self):
        return self.__dvd_id
    
    def get_email(self):
        return self.__email

    def get_rental_state(self):
        return self.__rental_state

    def get_values(self):
        return [self.__id, self.__physical_code, self.__dvd_id, self.__rental_state]

    @classmethod
    def get_by_row(cls, row):
        return PhysicalDVDModel(row[0], row[1], row[2], row[3])

