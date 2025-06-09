from pushdown_automata.terminal import *

class Inherited:
    def __init__(self, name: str, value: int | float | str | None = None):
        self.name = name
        self.ref: Sintetized
        self.value = value
        
        self.attr_users: list[Sintetized] = []
    
    def __str__(self):
        return self.name + "=" + (f"{self.value}" if self.value is not None else "None")
    
    __repr__ = __str__
        
class Sintetized:
    def __init__(self, name: str, ref: Inherited | Terminal | None = None):
        self.name = name
        self.ref: Inherited = ref
        
        self.attr_users: list[Inherited | 'Sintetized'] = []
    
    def __str__(self):
        return self.name + "=" + (f"{self.ref.value}" if self.ref is not None and self.ref.value is not None else "None")
    
    __repr__ = __str__
