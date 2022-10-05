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


def delete_by_id(sqlite_db, table_name, id):
    connection = sqlite3.connect(sqlite_db)
    cursor = connection.cursor()
    delete = cursor.execute(f'DELETE FROM {table_name} WHERE rowId = {id}')
    connection.commit()
