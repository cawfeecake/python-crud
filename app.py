from flask import Flask, render_template, url_for
from markupsafe import escape

from routes.database_api.database import \
    init_database as init_routes_database, \
    database_status, \
    get_all_tables


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

nav_funcs = []
with app.app_context():
    import routes.movies
    nav_funcs.append(('movies', 'get_movies'))

    import routes.items
    nav_funcs.append(('items', 'get_items'))

    #import routes.locations
    #nav_funcs.append(('locations', 'get_locations'))

init_routes_database(app)

@app.route('/')
def index():
    return render_template('index.html',
        nav_funcs=nav_funcs,
        all_tables=get_all_tables(),
        database_status=database_status(),
    )


# TODO remove below

# month is in range [1, 12]
@app.route('/cal/<int:month>/')
def add(month):
    # TODO render template?
    #return f'<h1>{month}</h1>'
    return render_template('base.html', title=month)

# TODO custom 404 (i.e. "item not found" vs. "anything else not found"
#@app.errorhandler(404)
#def four_o_four(e):
#    attrs = vars(e)
#    attrs_str = ', '.join("%s: %s" % item for item in attrs.items())
#    #return f'{ escape(e.response) }: { escape(attrs_str) }'
#    return f'{ escape(locals()) }'
