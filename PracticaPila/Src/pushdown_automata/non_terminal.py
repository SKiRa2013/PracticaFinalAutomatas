from pushdown_automata.attributes import *

class NoTerminal:
    def __init__(self, name: str):
        self.name = name
        
        self.inherited: list[Inherited] = []
        self.sintetized: list[Sintetized] = []
        
    def __str__(self):
        attributes = f"{self.inherited}" if len(self.inherited) > 0 else f""
        attributes += f", " if len(self.inherited) > 0 and len(self.sintetized) > 0 else f""
        attributes += f"{self.sintetized}" if len(self.sintetized) > 0 else f""
           
        return f"<{self.name}>" + ( f" ( {attributes} )" if len(self.inherited) > 0 or len(self.sintetized) > 0  else "" )
        
    def equals_nonterminal(self, nterm2: 'NoTerminal'):
        print(f"{self.name} equals {nterm2.name}?")
        
        if self.name != nterm2.name:
            print("Different name")
            return False
        
        for inh in self.inherited:
            if inh not in nterm2.inherited:
                print(f"Inherited {inh.name} not in {nterm2.name} not-terminal")
                return False
            
        for snt in self.sintetized:
            if snt not in nterm2.sintetized:
                print(f"Sintetized {snt.name} not in {nterm2.name} not-terminal")
                return False
        
        return True
    
    __repr__ = __str__
    
        
if __name__ == "__main__":
    ejemplo = NoTerminal("NT ejemplo")
    print(type(ejemplo).__name__)
    