import sqlite3


class Database:
    def __init__(self, sqlite_db, table_name, table_columns):
        self.sqlite_db = sqlite_db
        self.table_name = table_name
        self.table_columns = list(map(lambda tup: tup[0], table_columns))

        con = sqlite3.connect(self.sqlite_db, detect_types=sqlite3.PARSE_DECLTYPES)
        cur = con.cursor()
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name}({', '.join(map(lambda tup: tup[0] if tup[0] == tup[-1] else f'{tup[0]} {tup[-1]}', table_columns))})
        """)


    # Input(s):
    # * data: list [] of tuples () where fields are in order of table columns, e.g. [(col_0, col_1), ...]
    # Output:
    # * list [] of inserted IDs, e.g. [id_0, id_1, ...]
    def insert_data(self, data):
        con = sqlite3.connect(self.sqlite_db, detect_types=sqlite3.PARSE_DECLTYPES)
        cur = con.cursor()
        inserted_ids = []
        if isinstance(data, list):
            for datum in data:
                inserted_ids += [ self.__insert_data(cur, datum) ]
        else:
            inserted_ids = [ self.__insert_datum(cur, data) ]
        con.commit()
        return inserted_ids


    def __insert_data(self, cursor, datum):
        cursor.execute(f"""
            INSERT INTO {self.table_name}
            VALUES({' ,'.join(['?'] * len(self.table_columns))})""", datum)
        return cursor.lastrowid


    def get_by_id(self, id):
        con = sqlite3.connect(self.sqlite_db, detect_types=sqlite3.PARSE_DECLTYPES)
        cur = con.cursor()
        get_row = cur.execute(f"""
            SELECT * FROM {self.table_name} WHERE rowid = {id}
        """)
        return get_row.fetchone()


    def update_by_id(self, id, data):
        num_table_cols = len(self.table_columns)
        num_data_inserting = len(data)
        if num_table_cols != num_data_inserting:
            warning = f'data provided: requested {num_cols}; received {num_data}'
            if num_table_cols > num_data_inserting:
                warning = f'too few {warning}'
            elif num_table_cols < num_data_inserting:
                warning = f'too many {warning}'
            print(f'[WARNING] {warning}')

        con = sqlite3.connect(self.sqlite_db, detect_types=sqlite3.PARSE_DECLTYPES)
        cur = con.cursor()
        update_row = cur.execute(f"""
            UPDATE {self.table_name}
            SET { ', '.join(map(lambda tup: f'{tup[0]}="{tup[-1]}"', zip(self.table_columns, data))) }
            WHERE rowid = {id} AND { ' AND '.join(map(lambda col: f'NOT {col} IS NULL', self.table_columns)) }
        """)
        con.commit()


    def delete_by_id(self, id):
        con = sqlite3.connect(self.sqlite_db, detect_types=sqlite3.PARSE_DECLTYPES)
        cur = con.cursor()
        cur.execute(f"""
            DELETE FROM {self.table_name} WHERE rowid = {id}
        """)
        con.commit()


    def get_all(self):
        con = sqlite3.connect(self.sqlite_db, detect_types=sqlite3.PARSE_DECLTYPES)
        cur = con.cursor()
        get_all_rows = cur.execute(f"""
            SELECT rowid, * FROM {self.table_name}
        """)
        return get_all_rows.fetchall()
