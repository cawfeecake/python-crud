from flask import current_app as app, redirect, request, url_for


from databases.movies import *


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
        return redirect(url_for('get_movies'))
    all_movies = movies.get_all()
    return f"""
        <a href="{ url_for('index') }">&lt; Back</a>
        <form method="POST">
          <div><label>Name: <input type="text" name="name"></label></div>
          <div><label>Year: <input type="text" name="year"></label></div>
          <div><label>Rating Point: <input type="text" name="x"><input type="text" name="y"></label></div>
          <input type="submit" value="Create">
        </form>
        <hr />
        { f'<p>Inserted: { " ".join([str(i) for i in insert_ids]) }</p>' if insert_ids else '' }
        <ol>
          { ''.join([f'<li>{ get_html_movie(m) }</li>' for m in all_movies ]) }
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
        return redirect(url_for('get_movie_by_id', movie_id=movie_id)) # TODO continue to verify this has desired back-nav. behavior
        # note: when "waterfalling" from handling POST req., will add to your window history and make back-nav. difficult
    return f"""
        <a href="{ url_for('get_movies') }">&lt; Back</a>
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
              .then(() => {{ window.location.href = '{ url_for('get_movies') }'; }});
          }}
        </script>
    """
