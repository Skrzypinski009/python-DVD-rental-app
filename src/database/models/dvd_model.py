from .model import Model

class DVDModel(Model):
    TABLE_NAME = 'dvd'
    FIELDS_NAMES = ['id', 'name', 'date']
    def __init__(self, id, name, date):
        super().__init__(id)
        self.__name = name
        self.__date = date
    
### GETTERS ###
    def get_name(self):
        return self.__name

    def get_date(self):
        return self.__date

    def get_values(self):
        return [self.__id, self.__name, self.__date]

    @classmethod
    def get_by_row(cls, row):
        return DVDModel(row[0], row[1], row[2])

