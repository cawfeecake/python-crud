def convert_elements_to_str(arr):
    return [str(elem) for elem in arr]


class Children:
    def __init__(self, children):
        self.children = convert_elements_to_str(children)

    def __repr__(self):
        return f"Children({', '.join(self.children)})"


__separator = ';'


def adapt_children(c):
    return __separator.join(c.children).encode('utf-8')


def convert_children(c):
    children = list(map(str, c.split(bytes(__separator, 'utf-8'))))
    return Children(children)
