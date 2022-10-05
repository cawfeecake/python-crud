from .database import Database

items = Database('backend.db', 'items', [('name',), ('desc',), ('c', 'children')])

import sqlite3
from .types.children import adapt_children, convert_children, Children

sqlite3.register_adapter(Children, adapt_children)
sqlite3.register_converter('children', convert_children)
