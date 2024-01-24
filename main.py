from src.application import Application
from src.database.models import DVDModel
from src.database.database_manager import DatabaseManager
from datetime import date, datetime
# from src.database.fill_database import

if __name__ == "__main__":
    DatabaseManager.check_database()
    # DVDModel.insert({'name': 'aaa', 'date': datetime(2023, 2, 1)})
    # rows = DVDModel.select()
    # print(rows[0].get_id())
    app = Application()
    app.mainloop()


    
