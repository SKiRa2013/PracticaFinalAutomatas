from pushdown_automata.attributes import *

from typing import Protocol, Callable

class ActionMethod(Protocol):
    def __call__(self, *args: Inherited, dest: Sintetized | None):
        ...

class Action:
    def __init__(self, name: str):
        self.name = name
        self.all_executed = False
        
        self.execs: list[Callable[[], None]] = []
                
        self.inherited: list[Inherited] = []
        self.sintetized: list[Sintetized] = []
        
    def __str__(self):
        attributes = f"{self.inherited}" if len(self.inherited) > 0 else f""
        attributes += f", " if len(self.inherited) > 0 and len(self.sintetized) > 0 else f""
        attributes += f"{self.sintetized}" if len(self.sintetized) > 0 else f""
           
        return f"{{{self.name}}}" + ( f" ( {attributes} )".replace("[", "").replace("]", "") )
    
    __repr__ = __str__
    
    def add_exec(self, func: ActionMethod, *inh_source: Inherited, snt_dest: Sintetized | None):
        def wrapper_exec():
            func(*inh_source, snt_dest)
            
        self.execs.append(wrapper_exec)
    
    def exec(self):
        for ex in self.execs:
            ex()    
        
        self.all_executed = True
        
    def equals_action(self, act2: 'Action'):
        print(f"{self.name} equals {act2.name}?")
        
        if self.name != act2.name:
            print("Different name")
            return False
        
        for inh in self.inherited:
            if inh not in act2.inherited:
                print(f"Inherited {inh.name} not in {act2.name} not-terminal")
                return False

        for snt in self.sintetized:
            if snt not in act2.sintetized:
                print(f"Sintetized {snt.name} not in {act2.name} not-terminal")
                return False

        return True
        
if __name__ == "__main__":
    ejemplo = Action("NT ejemplo")
    print(type(ejemplo).__name__)
    