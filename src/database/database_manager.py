import sqlite3

class DatabaseManager:
    DB_PATH = "data/database.db"

    @classmethod
    def get_conn_cur(cls):
        conn = sqlite3.connect(cls.DB_PATH)
        cur = conn.cursor()
        return conn, cur

    @classmethod
    def close(cls, conn, cur):
        cur.close()
        conn.close()


    def check_database(self):
        conn, cur = self.get_conn_cur
        self.all_tables_create(cur, conn)
        self.close(conn, cur)

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
                       date TIMESTAMP);''')
        connection.commit()

    def category_table_create(self, cursor, connection):
            cursor.execute('''CREATE TABLE IF NOT EXIST category
                        (id INTEGER primary key autoincrement,
                        name TEXT);''')
            connection.commit()

    def dvd_category_relation_table_create(self, cursor, connection):
        cursor.execute('''CREATE TABLE IF NOT EXIST dvd_category_relation
                       (id INTEGER primary key autoincrement,
                       dvd_id INTEGER NOT NULL,
                       FOREIGN KEY (dvd_id));''')
        connection.commit()

    def physical_dvd_table_create(self, cursor, connection):
        cursor.execute('''CREATE TABLE IF NOT EXIST physical_dvd
                       (id INTEGER primary key autoincrement,
                       physical_code TEXT,
                       dvd_id INTEGER NOT NULL,
                       rental_state_id INTEGER NOT NULL,
                       FOREGIN KEY (rental_state_id),
                       FOREIGN KEY (dvd_id));''')
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
                       FOREIGN KEY (dvd_id));''')
        connection.commit()

### DELETING TABLES METHODS ###
    def all_tables_delete(self, cursor, connection):
        self.dvd_table_delete(cursor, connection)
        self.category_table_delete(cursor, connection)
        self.dvd_category_relation_table_delete(cursor, connection)
        self.physical_dvd_table_delete(cursor, connection)
        self.history_log_table_delete(cursor, connection)

    def dvd_table_delete(self, cursor, connection):
        cursor.execute('''DROP TABLE IF EXIST dvd;''')
        connection.commit()

    def category_table_delete(self, cursor, connection):
        cursor.execute('''DROP TABLE IF EXIST category;''')
        connection.commit()
        
    def dvd_category_relation_table_delete(self, cursor, connection):
        cursor.execute('''DROP TABLE IF EXIST dvd_category_relation;''')
        connection.commit()

    def physical_dvd_table_delete(self, cursor, connection):
        cursor,execute('''DROP TABLE IF EXIST physical_dvd;''')
        connection.commit()

    def history_log_table_delete(self, cursor, connection):
        cursor,execute('''DROP TABLE IF EXIST history_log;''')
        connection.commit()

### CLASS METHODS FOR MODELS ###
    @classmethod
    def get_name_eq_val(cls, fields_values, fields_names):
        arr_equals = []
        # dla wartości i indeksów id,name,date 
        for idx, col in enumerate(fields_values):
            # dodaj do arr_equals "<nazwa_pola> = <wartość_pola>"
            # tylko jeśli wartość nie jest równa None
            arr_equals.append(f"{fields_names[idx]} = {str(col)}") if col
        # połącz wartości arr_equals tekstem ", "
        return ", ".join(arr_equals)

    @classmethod
    def update(cls, table_name, fields_values, fields_names):
        conn, cur = cls.get_conn_cur()
        # set ustawia wartości poza id
        update_set = get_name_eq_val(fields_values[1:], fields_names[1:])
        # where zawiera tylko id = <wartość_id>
        where_id = f"{fields_names[0]} = {fields_values[0]}"
        cur.execute(f'''
            UPDATE {table_name}
            SET {update_set}
            WHERE {where_id};
        ''')
        conn.commit()
        cls.close(conn, cur)

    @classmethod
    def select(cls, table_name, fields_values, fields_names):
        conn, cur = cls.get_conn_cur()
        where = cls.get_name_eq_val([id,name,date], ["id","name","date"])
        cur.execute(f'''
            SELECT * FROM {table_name}
            WHERE {where};
        ''')
        rows = cur.fetchall()
        cls.close(conn, cur)
        return rows

    @classmethod
    def delete(cls, table_name, id):
        conn, cur = cls.get_conn_cur()
        cur.execute(f'''
            DELETE FROM {table_name}
            WHERE id = {id};
        ''')
        cls.close(conn, cur)

    @classmethod
    def delete_where(cls, table_name, fields_values, fields_names):
        conn, cur = cls.get_conn_cur()
        where = cls.get_name_eq_val([id,name,date], ["id","name","date"])
        cur.execute(f'''
            DELETE * FROM {table_name}
            WHERE {where};
        ''')
        cls.close(conn, cur)

