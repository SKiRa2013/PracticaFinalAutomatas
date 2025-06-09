
class Terminal:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return f"<{self.token_type}:{self.value}>"

    __repr__ = __str__
