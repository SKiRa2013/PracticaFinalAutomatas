
from grammar.attributes import Inherited, Synthesized

class NoTerminal:
    def __init__(self, name: str):
        self.name = name
        self.valor = None           # Resultado (numérico o booleano)
        self.relacional = False     # True si viene de una comparación
        self.valor_logico = None    # Valor lógico (opcional)

    def __str__(self):
        return f"<{self.name}: valor={self.valor}, relacional={self.relacional}>"

    __repr__ = __str__
