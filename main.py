from src.application import Application
from src.database.dvd_model import DVDModel
from src.database.database_manager import DatabaseManager
from datetime import date

if __name__ == "__main__":
    dbm = DatabaseManager()
    dbm.check_database()
    app = Application()
    app.mainloop()
    # rows = DVDModel.select()
    #
    # DVDModel.insert("Indiana Johnes", date(1999, 5, 12))
    # rows = DVDModel.select()
    # for row in rows:
    #     dvd_model = DVDModel.get_by_row(row)

    
