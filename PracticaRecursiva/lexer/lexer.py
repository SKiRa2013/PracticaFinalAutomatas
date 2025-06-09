import re

class Token:
    def __init__(self, type_, value):
        self.type = type_   # Tipo del token: NUM, ADD, MUL, ...
        self.value = value  # Valor real del token (ej: 5.5)

    def __str__(self):
        return f"{self.type}:{self.value}"

    def __repr__(self):
        return self.__str__()


class Lexer:
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.tokenize()

    def tokenize(self):
        # Definimos los patrones de tokens con expresiones regulares
        token_specification = [
            ('NUM',     r'\d+(\.\d+)?'),    # Números enteros o decimales
            ('AND',     r'&'),              # Operador lógico AND
            ('OR',      r'\|'),             # Operador lógico OR
            ('NOT',     r'NOT'),            # Operador lógico NOT (en mayúsculas)
            ('EQ',      r'=='),             # Igualdad
            ('NEQ',     r'!='),             # Diferente
            ('LE',      r'<='),             # Menor o igual
            ('GE',      r'>='),             # Mayor o igual
            ('LT',      r'<'),              # Menor que
            ('GT',      r'>'),              # Mayor que
            ('ADD',     r'\+'),             # Suma
            ('SUB',     r'-'),              # Resta
            ('MUL',     r'\*'),             # Multiplicación
            ('DIV',     r'/'),              # División
            ('EXP',     r'\^'),             # Exponente
            ('LPAREN',  r'\('),             # Paréntesis izquierdo
            ('RPAREN',  r'\)'),             # Paréntesis derecho
            ('SKIP',    r'[ \t]+'),         # Espacios y tabulaciones
            ('MISMATCH',r'.'),              # Cualquier otro carácter no reconocido
        ]

        regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

        for mo in re.finditer(regex, self.text):
            kind = mo.lastgroup
            value = mo.group()

            if kind == 'NUM':
                value = float(value)
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Token ilegal: {value}')

            self.tokens.append(Token(kind, value))

    def get_tokens(self):
        return self.tokens
