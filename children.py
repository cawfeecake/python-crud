__sqlite_str_encoding = 'utf-8'
__sqlite_str_separator = ';'


def adapt_children(c):
    return __sqlite_str_separator.join(c.children).encode(__sqlite_str_encoding)


def adapt_children_decoded(c):
    return adapt_children(c).decode(__sqlite_str_encoding)


class Children:
    def __init__(self, children):
        def convert_elements_to_str(arr):
            return [str(elem) for elem in arr]
        self.children = convert_elements_to_str(children)


    def __str__(self):
        return adapt_children_decoded(self)


    def __repr__(self):
        return f"Children({', '.join(self.children)})"


def convert_children(c):
    children = list(map(str, c.split(bytes(__sqlite_str_separator, __sqlite_str_encoding))))
    return Children(children)
