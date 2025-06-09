
class Inherited:
    def __init__(self, name: str, value=None):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name}={self.value}"

    __repr__ = __str__


class Synthesized:
    def __init__(self, name: str, value=None):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name}={self.value}"

    __repr__ = __str__
