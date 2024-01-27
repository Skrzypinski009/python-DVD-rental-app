from .model import Model

class ClientModel(Model):
    TABLE_NAME = 'client'
    FIELDS_NAMES = ['id', 'first_name', 'last_name', 'email', 'phone_number']
    def __init__(self, id, first_name, last_name, email, phone_number):
        super().__init__(id)
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__phone_number = phone_number
    
### GETTERS ###
    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name
    
    def get_email(self):
        return self.__email

    def get_phone_number(self):
        return self.__phone_number

    def get_values(self):
        return [self.__id, self.__first_name, self.__last_name, self.__email, self.__phone_number]

    @classmethod
    def get_by_row(cls, row):
        return ClientModel(row[0], row[1], row[2], row[3], row[4])

