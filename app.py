import os
from flask import Flask, url_for
from markupsafe import escape


from backend import db, path as db_path


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db.init_app(app)


# TODO custom 404 (i.e. "item not found" vs. "anything else not found"
#@app.errorhandler(404)
#def four_o_four(e):
#    attrs = vars(e)
#    attrs_str = ', '.join("%s: %s" % item for item in attrs.items())
#    #return f'{ escape(e.response) }: { escape(attrs_str) }'
#    return f'{ escape(locals()) }'


# for DEBUG
##############
from databases.database_tools import *

print(get_all_tables(db_path))

from sqlalchemy import create_engine
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f'# of tables: { len(tables) }')
for table_name in tables:
    print(f'{table_name}: { " | ".join(col["name"] for col in inspector.get_columns(table_name)) }')

# ad-hoc db changes
#delete_table(db_path, 'items')
#delete_by_id(db_path, 'movies', 14)
##############
# for DEBUG


index_funcs = []
with app.app_context():
    import routes.movies
    index_funcs.append(('movies', 'get_movies'))

    #import routes.locations
    #index_funcs.append(('locations', 'get_locations'))

    import routes.items
    index_funcs.append(('items', 'get_items'))


# TODO determine what we need to do here for adding tables...
#if not os.path.exists(DB_NAME):
with app.app_context():
    db.create_all()
    print(f'created tables in backend.')
    engine = db.get_engine()
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f'# of tables: { len(tables) }')
    for table_name in tables:
        print(f'{table_name}: { " | ".join(col["name"] for col in inspector.get_columns(table_name)) }')


@app.route('/')
def index():
    file_size = os.path.getsize(db_path)
    size_dim = 'bytes'
    if file_size > 1e7:
        size_dim = 'GB'
        file_size *= 1e-9
    elif file_size > 1e5:
        size_dim = 'MB'
        file_size *= 1e-6
    elif file_size > 1e3:
        size_dim = 'KB'
        file_size *= 1e-3

    return f"""
        <h1>Python C. R. U. D.</h1>
        <h2>Pages:</h2>
        <ul>
        { ''.join([ f'<li><a href="{ url_for(func) }">{ name }</a></li>' for (name, func) in index_funcs ]) }
        </ul>
        <h2>Backend Status:</h2>
        <p>file { db_path } is currently { round(file_size, 2) } { size_dim } in size</p>
    """
