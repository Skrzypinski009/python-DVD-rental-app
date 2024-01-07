import sqlite3
import os
import datetime

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
        if(type(val) == datetime.datetime):
            return f'{val.timestamp()}'

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
        self.client_table_create(cursor, connection)
        self.rental_state_table_create(cursor, connection)

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
    
    def client_table_create(self, cursor, connection):
        cursor.execute('''CREATE TABLE IF NOT EXISTS client (
                        id INTEGER PRIMARY KEY autoincrement,
                        first_name TEXT,
                        last_name TEXT,
                        email TEXT,
                        phone_number TEXT);''')
        connection.commit()

    def rental_state_table_create(self, cursor, connection):
        cursor.execute('''CREATE TABLE IF NOT EXISTS rental_state(
                       id INTEGER PRIMARY KEY autoincrement,
                       physical_dvd_id INTEGER NOT NULL REFERENCES physical_dvd,
                       state INTEGER);''')
        connection.commit()

### DELETING TABLES METHODS ###
    def all_tables_delete(self, cursor, connection):
        self.dvd_table_delete(cursor, connection)
        self.category_table_delete(cursor, connection)
        self.dvd_category_relation_table_delete(cursor, connection)
        self.physical_dvd_table_delete(cursor, connection)
        self.history_log_table_delete(cursor, connection)
        self.client_table_delete(cursor, connection)
        self.rental_state_table_delete(cursor, connection)

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
        cursor.execute('''DROP TABLE IF EXISTS physical_dvd;''')
        connection.commit()

    def history_log_table_delete(self, cursor, connection):
        cursor.execute('''DROP TABLE IF EXISTS history_log;''')
        connection.commit()

    def client_table_delete(self, cursor, connection):
        cursor.execute('''DROP TABLE IF EXIST client_table''')
        connection.commit()

    def rental_state_table_delete(self, cursor, connection):
        cursor.execute('''DROP TABLE IF EXIST rental_state''')
        connection.commit()

### CLASS METHODS FOR MODELS ###
    @classmethod
    def get_name_eq_val(cls, fields: dict):
        eq = []
        for key, val in fields.items():
            if type(val) == list:
                eq.append(f'{key} IN ({", ".join(cls.val_to_str(val))})')
            else:
                eq.append(f'{key} = {cls.val_to_str(val)}')
        return eq

    

    @classmethod
    def update(cls, table_name, id, fields):
        conn, cur = cls.get_conn_cur()
        if 'id' in fields.keys():
            fields.pop('id')
        update_set = ', '.join(get_name_eq_val(fields))
        where_id = f"id = {id}"
        cur.execute(f'''
            UPDATE {table_name}
            SET {update_set}
            WHERE {where_id};
        ''')
        conn.commit()
        cls.close(conn, cur)

    @classmethod
    def insert(cls, table_name, fields):
        conn, cur = cls.get_conn_cur()
        names = []
        values = []
        cmd = f'INSERT INTO {table_name}'
        for key, val in fields.items():
            values.append(cls.val_to_str(val))
            names.append(key)
        cmd += f' ({", ".join(names)})'
        cmd += f' VALUES ({", ".join(values)});'
        print(cmd)
        cur.execute(cmd)
        conn.commit()
        cls.close(conn, cur)



    @classmethod
    def select(cls, table_name, cols, where_fields, limit=None, offset=None):
        conn, cur = cls.get_conn_cur()
        where = ' AND '.join(cls.get_name_eq_val(where_fields))
        cmd = f'SELECT {", ".join(cols)} FROM {table_name}' 
        cmd += f' WHERE {where}' if where != '' else ''
        cmd += f' LIMIT {str(limit)}' if limit != None else ''
        cmd += f' OFFSET {str(offset)}' if offset != None else ''
        print(cmd)
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
    def delete_where(cls, table_name, fields):
        conn, cur = cls.get_conn_cur()
        where = ' AND '.join(cls.get_name_eq_val(fields))
        cmd = f'DELETE FROM {table_name}' 
        cmd += f' WHERE {where}' if where != '' else ''
        print(cmd)
        cur.execute(cmd)
        conn.commit()
        cls.close(conn, cur)

