from .database import Database

movies = Database('backend.db', 'movies', ['title', 'year', 'score point'])

import sqlite3
from point import *

sqlite3.register_adapter(Point, adapt_point)
sqlite3.register_converter('point', convert_point)
