from typing import Literal

class Terminal:
    def __init__(self, token_name: str, value: str | int | float | None = None):
        self.token_name = token_name
        self.value: str | int | float | None = value
    
    def equals_terminal(self, term2: 'Terminal') -> Literal[-1, 0, 1]:
        NOT_EQUALS = -1
        FAMILY_EQUALS = 0
        COMPLETELY_EQUALS = 1
        
        if self.token_name == term2.token_name:
            if self.value is None:
                return FAMILY_EQUALS
            
            if self.value == term2.value:
                return COMPLETELY_EQUALS
            
            return FAMILY_EQUALS
            
        return NOT_EQUALS
        
    def __str__(self):
        if self.token_name == "special" and self.value == "$":
            return "<empty-string>"
        
        return "<" + self.token_name + ("" if self.value is None else "_" + str(self.value)) + ">"
    
    __repr__ = __str__
    