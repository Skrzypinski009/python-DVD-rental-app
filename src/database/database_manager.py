import sqlite3
import os

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

    @classmethod
    def val_to_str(cls, val):
        if(type(val) == str):
            return f'"{val}"'
        return str(val)

    def check_database(self):
        if not 'data' in os.listdir():
            os.mkdir('data')
        conn, cur = self.get_conn_cur()
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
        cursor.execute('''CREATE TABLE IF NOT EXISTS dvd
                       (id INTEGER primary key autoincrement,
                       name TEXT,
                       date TIMESTAMP);''')
        connection.commit()

    def category_table_create(self, cursor, connection):
            cursor.execute('''CREATE TABLE IF NOT EXISTS category
                        (id INTEGER primary key autoincrement,
                        name TEXT);''')
            connection.commit()

    def dvd_category_relation_table_create(self, cursor, connection):
        cursor.execute('''CREATE TABLE IF NOT EXISTS dvd_category_relation
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       dvd_id INTEGER NOT NULL REFERENCES dvd,
                       category_id INTEGER NOT NULL REFERENCES category);''')
        connection.commit()

    def physical_dvd_table_create(self, cursor, connection):
        cursor.execute('''CREATE TABLE IF NOT EXISTS physical_dvd
                       (id INTEGER primary key autoincrement,
                       physical_code TEXT,
                       dvd_id INTEGER NOT NULL REFERENCES dvd,
                       rental_state_id INTEGER NOT NULL REFERENCES rental_state);''')
        connection.commit()

    def hisrory_log_table_create(self, cursor, connection):
        cursor.execute('''CREATE TABLE IF NOT EXISTS history_log
                       (id INTEGER primary key autoincrement,
                       time_date TIMESTAMP,
                       physical_dvd_id INTEGER NOT NULL REFERENCES physical_dvd,
                       rental_state_id INTEGER NOT NULL REFERENCES rental_state,
                       client_id INTEGER NOT NULL REFERENCES client);''')
        connection.commit()

### DELETING TABLES METHODS ###
    def all_tables_delete(self, cursor, connection):
        self.dvd_table_delete(cursor, connection)
        self.category_table_delete(cursor, connection)
        self.dvd_category_relation_table_delete(cursor, connection)
        self.physical_dvd_table_delete(cursor, connection)
        self.history_log_table_delete(cursor, connection)

    def dvd_table_delete(self, cursor, connection):
        cursor.execute('''DROP TABLE IF EXISTS dvd;''')
        connection.commit()

    def category_table_delete(self, cursor, connection):
        cursor.execute('''DROP TABLE IF EXISTS category;''')
        connection.commit()
        
    def dvd_category_relation_table_delete(self, cursor, connection):
        cursor.execute('''DROP TABLE IF EXISTS dvd_category_relation;''')
        connection.commit()

    def physical_dvd_table_delete(self, cursor, connection):
        cursor,execute('''DROP TABLE IF EXISTS physical_dvd;''')
        connection.commit()

    def history_log_table_delete(self, cursor, connection):
        cursor,execute('''DROP TABLE IF EXISTS history_log;''')
        connection.commit()

### CLASS METHODS FOR MODELS ###
    @classmethod
    def get_name_eq_val(cls, fields_values, fields_names):
        arr_equals = []
        # dla wartości i indeksów id,name,date 
        for idx, val in enumerate(fields_values):
            # dodaj do arr_equals "<nazwa_pola> = <wartość_pola>"
            # tylko jeśli wartość nie jest równa None
            if val != None:
                arr_equals.append(f"{fields_names[idx]} = {cls.val_to_str(val)}")
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
    def insert(cls, table_name, fields_values, fields_names):
        conn, cur = cls.get_conn_cur()
        names = []
        values = []
        cmd = f'INSERT INTO {table_name}'
        for idx, val in enumerate(fields_values):
            if val != None:
                values.append(cls.val_to_str(val))
                names.append(fields_names[idx])
        cmd += f' ({", ".join(names)})'
        cmd += f' VALUES ({", ".join(values)});'
        cur.execute(cmd)
        conn.commit()
        cls.close(conn, cur)



    @classmethod
    def select(cls, table_name, fields_values, fields_names, limit=None, offset=None):
        conn, cur = cls.get_conn_cur()
        where = cls.get_name_eq_val(fields_values, fields_names)
        cmd = f'SELECT * FROM {table_name}' 
        cmd += f' WHERE {where}' if where != '' else ''
        cmd += f' LIMIT {str(limit)}' if limit != None else ''
        cmd += f' OFFSET {str(offset)}' if offset != None else ''
        cur.execute(cmd)
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
        conn.commit()
        cls.close(conn, cur)

    @classmethod
    def delete_where(cls, table_name, fields_values, fields_names):
        conn, cur = cls.get_conn_cur()
        where = cls.get_name_eq_val(fields_values, fields_names)
        cmd = f'DELETE * FROM {table_name}' 
        cmd += f' WHERE {where}' if where != '' else ''
        cur.execute(cmd)
        conn.commit()
        cls.close(conn, cur)

