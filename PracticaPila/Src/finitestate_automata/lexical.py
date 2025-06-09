from kiratools.queue import *

class Lexical:
    def __init__(self):
        self.string = ""
        self.string_tape = Queue()
        
    def execute_analysis(self):
        pass
    
    def set_stringtape(self, stape: Queue):
        self.string_tape = stape
        