import json
from markupsafe import escape
from flask import Flask, abort, redirect, request, url_for


# Import depended on tables here
from databases.movies import *
from databases.items import *


app = Flask(__name__)


# for DEBUG;;
from databases.database_tools import *
# DEBUG;; TOREMOVE
print(get_all_tables('backend.db'))
# TROUBLESHOOTING;;
#delete_by_id('backend.db', 'movies', 14)
#delete_table('backend.db', 'items')


@app.route('/')
def index():
    return f"""
        <h1>What's in the "movies" table?</h1>
        <p>There are {len(movies.get_all())} movies in the database!</p>
    """


# data = [
#     ('Monty Python and the Holy Grail', 1975, p1),
#     ('And Now for Something Completely Different', 1971, p2),
#     ('Another movie', 1977, p3),
# ]
@app.route('/movies/', methods=['GET', 'POST'])
def get_movies():
    # write to movies if a POST request
    insert_ids = None # declare variables before if block if they are used outside scope
    if request.method == 'POST':
        movie_name = request.form.get('name')
        movie_year = request.form.get('year')
        rating_x, rating_y = (float(request.form.get('x')), float(request.form.get('y')))
        insert_ids = movies.insert_data([(movie_name, movie_year, Point(rating_x, rating_y))])
        # use a return here if you want to redirect away when doing POST
        #return f"""
        #    <h1>Added the movie: {movie_name}</h1>
        #    <pre>{insert_id[0]}</pre>
        #"""
    all_movies = movies.get_all()
    return f"""
        <form method="POST">
          <div><label>Name: <input type="text" name="name"></label></div>
          <div><label>Year: <input type="text" name="year"></label></div>
          <div><label>Rating Point: <input type="text" name="x"><input type="text" name="y"></label></div>
          <input type="submit" value="Submit">
        </form>
        <hr />
        { f'<p>Inserted: { " ".join([str(i) for i in insert_ids]) }</p>' if insert_ids else '' }
        <ol>
          <li>{ '</li><li>'.join(get_html_movie(m) for m in all_movies) }</li>
        </ol>
    """


def get_html_movie(movie):
    movie_id = movie[0]
    movie_name = movie[1]
    movie_year = movie[2]
    return f"""
        <div>
          <a href="{ url_for('get_movie_by_id', movie_id=movie_id) }">{movie_name}, ({movie_year})</a>
        </div>
    """


# TODO if able, use PUT instead of POST as it is more appropriate as it is an update
@app.route('/movies/<int:movie_id>/', methods=['GET', 'DELETE', 'POST'])
def get_movie_by_id(movie_id):
    if request.method == 'DELETE':
        movies.delete_by_id(movie_id)
        return 'OK', 204
    elif request.method == 'POST':
        movie_name = request.form.get('name')
        movie_year = request.form.get('year')
        rating_x, rating_y = (float(request.form.get('x')), float(request.form.get('y')))
        update_data = [movie_name, movie_year, Point(rating_x, rating_y)]
        movies.update_by_id(movie_id, update_data)
        # have this method handler "waterfall" into default (i.e. GET) request path; will get current info for $movie_id
    return f"""
        <p>{ movies.get_by_id(movie_id) }</p>
        <hr />
        <form method="POST">
          <div><label>Name: <input type="text" name="name"></label></div>
          <div><label>Year: <input type="text" name="year"></label></div>
          <div><label>Rating Point: <input type="text" name="x"><input type="text" name="y"></label></div>
          <input type="submit" value="Update">
        </form>
        <button onclick="delete_movie()">Delete</button>
        <script>
          function delete_movie() {{
            const delete_url = '{ url_for('get_movie_by_id', movie_id=movie_id) }';
            fetch(delete_url, {{ method: 'DELETE' }})
              .then(() => {{ window.location.href = '{ url_for('get_movies') }'; }})
          }}
        </script>
    """


# data = [
#     ('name', 'desc', children) ...,
#     ('comb', 'used to brush my hair', []),
#     ('cabinet', '3 stacked plastic drawers', [-1]),
# ]
@app.route('/items/', methods=['GET', 'POST'])
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


@app.route('/items/<int:item_id>/', methods=['GET', 'DELETE', 'POST'])
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
@app.route('/about/')
def about():
    return '<h3>This is a Flask web application.</h3>'

@app.route('/capitalize/<word>/')
def capitalize(word):
    return '<h1>{}</h1>'.format(escape(word.capitalize()))

@app.route('/add/<int:n1>/<int:n2>/')
def add(n1, n2):
    return '<h1>{}</h1>'.format(n1 + n2)

@app.route('/users/<int:user_id>/')
def greet_user(user_id):
    users = ['Bob', 'Jane', 'Adam']
    try:
        return '<h2>Hi {}</h2>'.format(users[user_id])
    except IndexError:
        abort(404)
