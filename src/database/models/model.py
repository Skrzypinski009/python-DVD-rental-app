from src.database.database_manager import DatabaseManager

class Model:
    TABLE_NAME = ""
    FIELDS_NAMES = ['id']
    def __init__(self, id):
        self.__id = id

### GETTERS ###
    def get_id(self):
        return self.__id

    @classmethod
    def get_fields_names(cls):
        return __FIELDS_NAMES

    def get_values(self):
        return [self.__id]

    def get_fields(self):
        return dict(zip(__FIELDS_NAMES, self.__get_values()))

### DATABASE METHODS ###
    def update(self, fields):
        print(fields)
        DatabaseManager.update(self.TABLE_NAME, self.__id, fields)
        return self.select({'id': self.__id})

    def delete(self):
        DatabaseManager.delete(self.TABLE_NAME, self.__id)

### DATABASE CLASS METHODS ###
    @classmethod
    def insert(cls, fields):
        DatabaseManager.insert(cls.TABLE_NAME, fields)
        return cls.select(fields)

    @classmethod
    def select(cls, where_fields={}, like_fields={}, limit=None, offset=None, order_col=None, desc=None):
        return [cls.get_by_row(row) for row in DatabaseManager.select(
            cls.TABLE_NAME, cls.FIELDS_NAMES, where_fields, like_fields, limit, offset, order_col, desc)]
    
    @classmethod
    def delete_where(cls, fields={}):
        return DatabaseManager.delete_where(cls.TABLE_NAME, fields)

