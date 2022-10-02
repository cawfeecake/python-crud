class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

def adapt_point(point):
    return f"{point.x};{point.y}".encode("utf-8")

def convert_point(s):
    x, y = list(map(float, s.split(b";")))
    return Point(x, y)
