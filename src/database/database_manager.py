import sqlite3
import os
import datetime

class DatabaseManager:
    DB_PATH = "data/database.db"

    # stałe dla rental state
    RETURNED = 0 # (NOT_BORROWED)
    BORROWED = 1

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

    @classmethod
    def check_database(cls):
        if not 'data' in os.listdir():
            os.mkdir('data')
        cls.all_tables_create()

### CREATING TABLES METHODS ###
    @classmethod
    def all_tables_create(cls):
        conn, cur = cls.get_conn_cur();
        cls.dvd_table_create(cur, conn)
        cls.category_table_create(cur, conn)
        cls.dvd_category_relation_table_create(cur, conn)
        cls.physical_dvd_table_create(cur, conn)
        cls.hisrory_log_table_create(cur, conn)
        cls.client_table_create(cur, conn)
        cls.close(conn, cur)

    @classmethod
    def dvd_table_create(cls, cur, conn):
        cur.execute('''CREATE TABLE IF NOT EXISTS dvd
                       (id INTEGER primary key autoincrement,
                       name TEXT,
                       date TIMESTAMP);''')
        conn.commit()

    @classmethod
    def category_table_create(cls, cur, conn):
            cur.execute('''CREATE TABLE IF NOT EXISTS category
                        (id INTEGER primary key autoincrement,
                        name TEXT);''')
            conn.commit()

    @classmethod
    def dvd_category_relation_table_create(cls, cur, conn):
        cur.execute('''CREATE TABLE IF NOT EXISTS dvd_category_relation
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       dvd_id INTEGER NOT NULL REFERENCES dvd,
                       category_id INTEGER NOT NULL REFERENCES category);''')
        conn.commit()

    @classmethod
    def physical_dvd_table_create(cls, cur, conn):
        cur.execute('''CREATE TABLE IF NOT EXISTS physical_dvd
                       (id INTEGER primary key autoincrement,
                       physical_code TEXT,
                       rental_state INTEGER NOT NULL,
                       dvd_id INTEGER NOT NULL REFERENCES dvd
                       );''')
        conn.commit()

    @classmethod
    def hisrory_log_table_create(cls, cur, conn):
        cur.execute('''CREATE TABLE IF NOT EXISTS history_log
                       (id INTEGER primary key autoincrement,
                       time_date TIMESTAMP,
                       physical_dvd_id INTEGER NOT NULL REFERENCES physical_dvd,
                       rental_state INTEGER NOT NULL,
                       client_id INTEGER NOT NULL REFERENCES client);''')
        conn.commit()
    
    @classmethod
    def client_table_create(cls, cur, conn):
        cur.execute('''CREATE TABLE IF NOT EXISTS client (
                        id INTEGER PRIMARY KEY autoincrement,
                        first_name TEXT,
                        last_name TEXT,
                        email TEXT,
                        phone_number TEXT);''')
        conn.commit()

### DELETING TABLES METHODS ###
    @classmethod
    def all_tables_delete(cls):
        conn, cur = cls.get_conn_cur()
        cls.dvd_table_delete(cur, conn)
        cls.category_table_delete(cur, conn)
        cls.dvd_category_relation_table_delete(cur, conn)
        cls.physical_dvd_table_delete(cur, conn)
        cls.history_log_table_delete(cur, conn)
        cls.client_table_delete(cur, conn)
        cls.close(conn, cur)

    @classmethod
    def dvd_table_delete(cls, cur, conn):
        cur.execute('''DROP TABLE IF EXISTS dvd;''')
        conn.commit()

    @classmethod
    def category_table_delete(cls, cur, conn):
        cur.execute('''DROP TABLE IF EXISTS category;''')
        conn.commit()
        
    @classmethod
    def dvd_category_relation_table_delete(cls, cur, conn):
        cur.execute('''DROP TABLE IF EXISTS dvd_category_relation;''')
        conn.commit()

    @classmethod
    def physical_dvd_table_delete(cls, cur, conn):
        cur.execute('''DROP TABLE IF EXISTS physical_dvd;''')
        conn.commit()

    @classmethod
    def history_log_table_delete(cls, cur, conn):
        cur.execute('''DROP TABLE IF EXISTS history_log;''')
        conn.commit()

    @classmethod
    def client_table_delete(cls, cur, conn):
        cur.execute('''DROP TABLE IF EXISTS client_table''')
        conn.commit()

### CLASS METHODS FOR MODELS ###
    @classmethod
    def get_name_eq_val(cls, fields: dict):
        eq = []
        for key, val in fields.items():
            if type(val) == list:
                eq.append(f'{key} IN ({", ".join([ cls.val_to_str(v) for v in val ])})')
            else:
                eq.append(f'{key} = {cls.val_to_str(val)}')
        return eq

    @classmethod
    def update(cls, table_name, id, fields):
        print(fields)
        conn, cur = cls.get_conn_cur()
        if 'id' in fields.keys():
            fields.pop('id')
        update_set = ', '.join(cls.get_name_eq_val(fields))
        where_id = f"id = {id}"
        cmd = f"UPDATE {table_name} SET {update_set} WHERE {where_id};"
        cur.execute(cmd)
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
    def select(cls, table_name, cols, where_fields, limit=None, offset=None, order_col=None, desc=None):
        conn, cur = cls.get_conn_cur()
        where = ' AND '.join(cls.get_name_eq_val(where_fields))
        cmd = f'SELECT {", ".join(cols)} FROM {table_name}' 
        cmd += f' WHERE {where}' if where != '' else ''
        cmd += f' ORDER BY {order_col}' if order_col != None else ''
        cmd += ' DESC' if desc != None else ''
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
        cmd = f" DELETE FROM {table_name} WHERE id = {id};"
        print(cmd)
        cur.execute(cmd)
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

