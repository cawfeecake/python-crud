import sqlite3


class Database:
    def __init__(self, sqlite_db, table_name, table_columns):
        self.sqlite_db = sqlite_db
        self.table_name = table_name
        self.table_columns = table_columns

        con = sqlite3.connect(self.sqlite_db, detect_types=sqlite3.PARSE_DECLTYPES)
        cur = con.cursor()
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name}({', '.join(self.table_columns)})
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


    def get_all(self):
        con = sqlite3.connect(self.sqlite_db, detect_types=sqlite3.PARSE_DECLTYPES)
        cur = con.cursor()
        get_all_rows = cur.execute(f"""
            SELECT rowid, * FROM {self.table_name}
        """)
        return get_all_rows.fetchall()
