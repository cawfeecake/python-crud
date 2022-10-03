import sqlite3


def get_all_tables(sqlite_db):
    connection = sqlite3.connect(sqlite_db)
    cursor = connection.cursor()
    get_tables = cursor.execute('SELECT name FROM sqlite_master')
    return get_tables.fetchall()


def delete_table(sqlite_db, table_name):
    connection = sqlite3.connect(sqlite_db)
    cursor = connection.cursor()
    drop = cursor.execute(f'DROP TABLE {table_name}')
    connection.commit()
