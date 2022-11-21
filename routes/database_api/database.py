import os

from flask_sqlalchemy import SQLAlchemy


db_path = 'backend.db'
_db_uri = f'sqlite:///{db_path}'

db = SQLAlchemy()


def init_database(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = _db_uri
    db.init_app(app)
    with app.app_context():
        db.create_all()

def database_status():
    file_size = os.path.getsize(db_path)
    size_dimension = 'bytes'
    if file_size > 1e7:
        size_dimension = 'GB'
        file_size *= 1e-9
    elif file_size > 1e5:
        size_dimension = 'MB'
        file_size *= 1e-6
    elif file_size > 1e3:
        size_dimension = 'KB'
        file_size *= 1e-3

    return {
        'file': db_path,
        'size': {
            'quantity': round(file_size, 2),
            'dimension': size_dimension,
        },
    }

from sqlalchemy import create_engine, inspect

def get_all_tables():
    engine = create_engine(_db_uri)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    cols_by_table = {}
    for table_name in tables:
        cols_by_table[table_name] = [ col['name'] for col in inspector.get_columns(table_name) ]
    return cols_by_table
