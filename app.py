import os
from flask import Flask, request, url_for # remove request after moving all routes


_app = Flask(__name__)


def create_backend(app, db_path):
    from flask_sqlalchemy import SQLAlchemy

    db = SQLAlchemy()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    db.init_app(app)

    # toggle this to determine what we need for adding tables, etc.
    #if not os.path.exists(DB_NAME):
    #    with app.app_context():
    #        db.create_all()
    #    print(f'created tables in backend.')


_db_path = 'backend.db'
create_backend(_app, _db_path)


index_funcs = []
with _app.app_context():
    import routes.movies
    index_funcs.append(('movies', 'get_movies'))

    #import routes.locations
    #index_funcs.append(('locations', 'get_locations'))

    import routes.items
    index_funcs.append(('items', 'get_items'))


@_app.route('/')
def index():
    file_size = os.path.getsize(_db_path)
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
        <p>file { _db_path } is currently { round(file_size, 2) } { size_dim } in size</p>
    """


# ====================================


# for DEBUG;;
from databases.database_tools import *
# DEBUG;; TOREMOVE
print(get_all_tables(_db_path))
# TROUBLESHOOTING;;
#delete_by_id(_db_path, 'movies', 14)
#delete_table(_db_path, 'items')


# TODO: TOREMOVE
#@_app.route('/about/')
#def about():
#    return '<h3>This is a Flask web application.</h3>'
#
#from markupsafe import escape
#@_app.route('/capitalize/<word>/')
#def capitalize(word):
#    return '<h1>{}</h1>'.format(escape(word.capitalize()))
#
#@_app.route('/add/<int:n1>/<int:n2>/')
#def add(n1, n2):
#    return '<h1>{}</h1>'.format(n1 + n2)
#
#...from flask import abort
#@_app.route('/users/<int:user_id>/')
#def greet_user(user_id):
#    users = ['Bob', 'Jane', 'Adam']
#    try:
#        return '<h2>Hi {}</h2>'.format(users[user_id])
#    except IndexError:
#        abort(404)
