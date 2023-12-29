import sqlite3

class DatabaseManager:
    def __init__(self):
        self.check_database()

    def check_database(self):
        conn = sqlite3.connect("data/database.db")
        cur = conn.cursor()
        self.all_tables_create()
        cur.close()
        conn.close()

    def all_tables_create(self, cursor, connection):
        self.dvd_table_create(cursor, connection)

        # kolejne tworzenie tabel

    def dvd_table_create(self, cursor, connection):
        cursor.execute('''CREATE TABLE IF NOT EXIST dvd
                       (id INTEGER primary key autoincrement
                       name TEXT
                       date TIMESTAMP)''')
        connection.commit()

    def all_tables_delete(self, cursor, connection):
        self.dvd_table_delete(cursor, connection)
        #kolejne usuwanie tabel

    def dvd_table_delete(self, cursor, connection):
        cursor.execute('''DROP TABLE IF EXIST dvd''')
        connection.commit()


    def category_table_create(self, cursor, connection):
            cursor.execute('''CREATE TABLE IF NOT EXIST category
                        (id INTEGER primary key autoincrement
                        name TEXT)''')
            
            
            connection.commit()
