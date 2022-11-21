from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect


db_path = 'backend.db'

db = SQLAlchemy()

def init_database(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    db.init_app(app)
    with app.app_context():
        db.create_all()

def get_all_tables():
    engine = db.get_engine()
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    cols_by_table = {}
    for table_name in tables:
        cols_by_table[table_name] = [
            col['name'] for col in inspector.get_columns(table_name)
        ]
    return cols_by_table
