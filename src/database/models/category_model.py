from .model import Model

class CategoryModel(Model):
    TABLE_NAME = 'category'
    FIELDS_NAMES = ['id', 'name']
    def __init__(self, id, name):
        super().__init__(id)
        self.__name = name
    
### GETTERS ###
    def get_name(self):
        return self.__name

    def get_values(self):
        return [self.__id, self.__name]

    @classmethod
    def get_by_row(cls, row):
        return CategoryModel(row[0], row[1])

