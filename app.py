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
    #index_funcs.append('locations')
    #index_funcs.append(('locations', 'get_locations'))

    #import routes.items
    #index_funcs.append('items')
    #index_funcs.append(('items', 'get_items'))


@_app.route('/')
def index():
    # TODO add stats about backend.db file
    return f"""
        <h1>Python C. R. U. D.</h1>
        <h2>Pages:</h2>
        <ul>
        { ''.join([ f'<li><a href="{ url_for(func) }">{ name }</a></li>' for (name, func) in index_funcs ]) }
        </ul>
        <h2>Backend stats:</h2>
        <p>for file {_db_path}...</p>
    """


# ====================================


# Import depended on tables here
from databases.items import *


# for DEBUG;;
from databases.database_tools import *
# DEBUG;; TOREMOVE
print(get_all_tables(_db_path))
# TROUBLESHOOTING;;
#delete_by_id(_db_path, 'movies', 14)
#delete_table(_db_path, 'items')


# data = [
#     ('name', 'desc', children) ...,
#     ('comb', 'used to brush my hair', []),
#     ('cabinet', '3 stacked plastic drawers', [-1]),
# ]
@_app.route('/items/', methods=['GET', 'POST'])
def get_items():
    insert_ids = None
    if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('desc')
        child = request.form.get('child')
        insert_ids = items.insert_data([(name, desc, Children([child, 1]))])
    all_items = items.get_all()
    return f"""
        <form method="POST">
          <div><label>Name: <input type="text" name="name"></label></div>
          <div><label>Description: <input type="text" name="desc"></label></div>
          <div><label>A child: <input type="text" name="child"></label></div>
          <input type="submit" value="Submit">
        </form>
        <hr />
        { f'<p>Inserted: { " ".join([str(i) for i in insert_ids]) }</p>' if insert_ids else '' }
        <p>Count: {len(all_items)}</p>
        <p>{all_items}</p>
    """


@_app.route('/items/<int:item_id>/', methods=['GET', 'DELETE', 'POST'])
def get_item_by_id(item_id):
    if request.method == 'DELETE':
        items.delete_by_id(item_id)
        return 'OK', 204
    elif request.method == 'POST':
        movie_name = request.form.get('name')
        movie_year = request.form.get('year')
        rating_x, rating_y = (float(request.form.get('x')), float(request.form.get('y')))
        update_data = [movie_name, movie_year, Point(rating_x, rating_y)]
        items.update_by_id(item_id, update_data)
    return f"""
        <p>{items.get_by_id(item_id)}</p>
        <hr />
        <form method="POST">
          <div><label>Name: <input type="text" name="name"></label></div>
          <div><label>Year: <input type="text" name="year"></label></div>
          <div><label>Rating Point: <input type="text" name="x"><input type="text" name="y"></label></div>
          <input type="submit" value="Update">
        </form>
    """


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
