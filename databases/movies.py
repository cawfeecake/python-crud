from .database import Database

movies = Database('backend.db', 'movies', [('title',), ('year',), ('score', 'point')])

import sqlite3
from .types.point import adapt_point, convert_point, Point

sqlite3.register_adapter(Point, adapt_point)
sqlite3.register_converter('point', convert_point)
