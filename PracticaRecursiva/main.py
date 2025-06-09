import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lexer.lexer import Lexer
from parser.recursive_parser import RecursiveParser

def ejecutar_expresion(expr: str):
    try:
        print("=" * 60)
        print(f"Expresión: {expr}")

        # Análisis Léxico
        lexer = Lexer(expr)
        tokens = lexer.get_tokens()

        # Imprime los tokens
        print("Tokens:")
        for token in tokens:
            print(f"  {token}")

        #Análisis sintáctico 
        parser = RecursiveParser(tokens)
        resultado = parser.parse()

        print(f"Resultado final: {resultado['valor']}")
    
    except SyntaxError as e:
        print(f"Error de sintaxis: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ejemplo = [
        "((5,5/3)+10)>20&20.5<10",            # Rechace
        "((5.5/3)+10)>20&20.5<10",            # Acepte I guess
        "5>3 & 3",
        "5>3 & 3"
    ]

    for expr in ejemplo:
        ejecutar_expresion(expr)
