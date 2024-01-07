from src.application import Application
from src.database.models import DVDModel
from src.database.database_manager import DatabaseManager
from datetime import date, datetime

if __name__ == "__main__":
    DVDModel.delete_where()
    DVDModel.insert({
        'name': "Indiana Johnes", 
        'date': datetime(1999, 5, 12) })
    DVDModel.insert({
        'name': "Batman 2", 
        'date': datetime(1999, 5, 12) })
    dvd_models = DVDModel.select()
    for dvd_model in dvd_models:
        print(dvd_model.get_values())

    dbm = DatabaseManager()
    dbm.check_database()
    app = Application()
    app.mainloop()


    
