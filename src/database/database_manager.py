import sqlite3

class DatabaseManager:
    def check_database(self):
        conn = sqlite3.connect("data/database.db")
        cur = conn.cursor()
        self.all_tables_create()
        cur.close()
        conn.close()

### CREATING TABLES METHODS ###
    def all_tables_create(self, cursor, connection):
        self.dvd_table_create(cursor, connection)
        self.category_table_create(cursor, connection)
        self.dvd_category_relation_table_create(cursor, connection)
        self.physical_dvd_table_create(cursor, connection)
        self.hisrory_log_table_create(cursor, connection)

    def dvd_table_create(self, cursor, connection):
        cursor.execute('''CREATE TABLE IF NOT EXIST dvd
                       (id INTEGER primary key autoincrement,
                       name TEXT,
                       date TIMESTAMP)''')
        connection.commit()

    def category_table_create(self, cursor, connection):
            cursor.execute('''CREATE TABLE IF NOT EXIST category
                        (id INTEGER primary key autoincrement,
                        name TEXT)''')
            connection.commit()

    def dvd_category_relation_table_create(self, cursor, connection):
        cursor.execute('''CREATE TABLE IF NOT EXIST dvd_category_relation
                       (id INTEGER primary key autoincrement,
                       dvd_id INTEGER NOT NULL,
                       FOREIGN KEY (dvd_id))''')
        connection.commit()

    def physical_dvd_table_create(self, cursor, connection):
        cursor.execute('''CREATE TABLE IF NOT EXIST physical_dvd
                       (id INTEGER primary key autoincrement,
                       physical_code TEXT,
                       dvd_id INTEGER NOT NULL,
                       rental_state_id INTEGER NOT NULL,
                       FOREGIN KEY (rental_state_id),
                       FOREIGN KEY (dvd_id))''')
        connection.commit()

    def hisrory_log_table_create(self, cursor, connection):
        cursor.execute('''CREATE TABLE IF NOT EXIST history_log
                       (id INTEGER primary key autoincrement,
                       time_date TIMESTAMP,
                       physical_dvd_id INTEGER NOT NULL,
                       rental_state_id INTEGER NOT NULL,
                       client_id INTEGER NOT NULL,
                       FOREGIN KEY (rental_state_id),
                       FOREGIN KEY (client_id),
                       FOREIGN KEY (dvd_id))''')
        connection.commit()

### DELETING TABLES METHODS ###
    def all_tables_delete(self, cursor, connection):
        self.dvd_table_delete(cursor, connection)
        self.category_table_delete(cursor, connection)
        self.dvd_category_relation_table_delete(cursor, connection)
        self.physical_dvd_table_delete(cursor, connection)
        self.history_log_table_delete(cursor, connection)

    def dvd_table_delete(self, cursor, connection):
        cursor.execute('''DROP TABLE IF EXIST dvd''')
        connection.commit()

    def category_table_delete(self, cursor, connection):
        cursor.execute('''DROP TABLE IF EXIST category''')
        connection.commit()
        
    def dvd_category_relation_table_delete(self, cursor, connection):
        cursor.execute('''DROP TABLE IF EXIST dvd_category_relation''')
        connection.commit()

    def physical_dvd_table_delete(self, cursor, connection):
        cursor,execute('''DROP TABLE IF EXIST physical_dvd''')
        connection.commit()

    def history_log_table_delete(self, cursor, connection):
        cursor,execute('''DROP TABLE IF EXIST history_log''')
        connection.commit()
