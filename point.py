__sqlite_str_encoding = 'utf-8'
__sqlite_str_separator = ';'


def adapt_point(point):
    return f'{point.x}{__sqlite_str_separator}{point.y}'.encode(__sqlite_str_encoding)


def adapt_point_decoded(point):
    return adapt_point(point).decode(__sqlite_str_encoding)


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y


    def __str__(self):
        return adapt_point_decoded(self)


    def __repr__(self):
        return f'Point({self.x}, {self.y})'


def convert_point(s):
    x, y = list(map(float, s.split(bytes(__sqlite_str_separator, __sqlite_str_encoding))))
    return Point(x, y)
