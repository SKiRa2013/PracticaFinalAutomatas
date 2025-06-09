from lexer.lexer import Token
from grammar.non_terminal import NoTerminal

class RecursiveParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0  # posición actual

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token("EOF", None)

    def match(self, expected_type):
        tok = self.current_token()
        if tok.type == expected_type:
            self.pos += 1
            return tok
        else:
            raise SyntaxError(f"Se esperaba {expected_type} pero se encontró {tok.type}")

    ##PARSE QUE NO OBLIGA PARENTESIS 
    def parse(self):
        print("Iniciando análisis sintáctico...")
        resultado = self.parse_ELO()
        if self.current_token().type != "EOF":
            raise SyntaxError("Tokens sobrantes al final de la expresión")
        return resultado

    # Producción inicial: S → ( ELO )
    def parse_S(self):
        print("Regla: S → ( ELO )")
        self.match("LPAREN")
        resultado = self.parse_ELO()
        self.match("RPAREN")
        return resultado

    def parse_ELO(self):
        print("Regla: ELO → EL2 ELO_L")
        left = self.parse_EL2()
        return self.parse_ELO_L(left)

    def parse_ELO_L(self, inherited):
        tok = self.current_token()
        if tok.type == "OR":
            print("Regla: ELO_L → | EL2 ELO_L")
            self.match("OR")
            right = self.parse_EL2()
            if not inherited["relacional"] or not right["relacional"]:
                raise SyntaxError("Los operandos de OR deben ser expresiones relacionales")
            resultado = inherited["valor"] or right["valor"]
            return self.parse_ELO_L({"valor": resultado, "relacional": True})

        elif tok.type in {"RPAREN", "AND", "EOF"}:
            print("Regla: ELO_L → ε")
            return inherited
        else:
            raise SyntaxError(f"Token inesperado en ELO_L: {tok.type}")

    def parse_EL2(self):
        print("Regla: EL2 → ER EL2_L")
        left = self.parse_ER()
        return self.parse_EL2_L(left)

    def parse_EL2_L(self, inherited):
        tok = self.current_token()
        if tok.type == "AND":
            print("Regla: EL2_L → & ER EL2_L")
            self.match("AND")
            right = self.parse_ER()
            if not inherited["relacional"] or not right["relacional"]:
                raise SyntaxError("Los operandos de AND deben ser expresiones relacionales")
            resultado = inherited["valor"] and right["valor"]
            return self.parse_EL2_L({"valor": resultado, "relacional": True})

        elif tok.type in {"RPAREN", "OR", "EOF"}:
            print("Regla: EL2_L → ε")
            return inherited
        else:
            raise SyntaxError(f"Token inesperado en EL2_L: {tok.type}")

    def parse_ER(self):
        print("Regla: ER → E ER_L")
        left = self.parse_E()
        return self.parse_ER_L(left)

    def parse_ER_L(self, inherited):
        tok = self.current_token()

        if tok.type in {"LT", "GT", "EQ", "NEQ", "LE", "GE"}:
            print(f"Regla: ER_L → {tok.type} E")
            op = tok.type
            self.match(op)
            right = self.parse_E()
            if op == "LT":
                result = inherited["valor"] < right["valor"]
            elif op == "GT":
                result = inherited["valor"] > right["valor"]
            elif op == "EQ":
                result = inherited["valor"] == right["valor"]
            elif op == "NEQ":
                result = inherited["valor"] != right["valor"]
            elif op == "LE":
                result = inherited["valor"] <= right["valor"]
            elif op == "GE":
                result = inherited["valor"] >= right["valor"]
            return {"valor": result, "relacional": True}

        elif tok.type in {"RPAREN", "OR", "AND", "EOF"}:
            print("Regla: ER_L → ε")
            return {"valor": inherited["valor"], "relacional": False}
        else:
            raise SyntaxError(f"Token inesperado en ER_L: {tok.type}")

    def parse_E(self):
        print("Regla: E → T E_L")
        left = self.parse_T()
        return self.parse_E_L(left)

    def parse_E_L(self, inherited):
        tok = self.current_token()
        if tok.type == "ADD":
            print("Regla: E_L → + T E_L")
            self.match("ADD")
            right = self.parse_T()
            result = inherited["valor"] + right["valor"]
            return self.parse_E_L({"valor": result})

        elif tok.type == "SUB":
            print("Regla: E_L → - T E_L")
            self.match("SUB")
            right = self.parse_T()
            result = inherited["valor"] - right["valor"]
            return self.parse_E_L({"valor": result})

        elif tok.type in {"RPAREN", "LT", "GT", "EQ", "NEQ", "LE", "GE", "AND", "OR", "EOF"}:
            print("Regla: E_L → ε")
            return inherited
        else:
            raise SyntaxError(f"Token inesperado en E_L: {tok.type}")

    def parse_T(self):
        print("Regla: T → P T_L")
        left = self.parse_P()
        return self.parse_T_L(left)

    def parse_T_L(self, inherited):
        tok = self.current_token()
        if tok.type == "MUL":
            print("Regla: T_L → * P T_L")
            self.match("MUL")
            right = self.parse_P()
            result = inherited["valor"] * right["valor"]
            return self.parse_T_L({"valor": result})

        elif tok.type == "DIV":
            print("Regla: T_L → / P T_L")
            self.match("DIV")
            right = self.parse_P()
            result = inherited["valor"] / right["valor"]
            return self.parse_T_L({"valor": result})

        elif tok.type in {"ADD", "SUB", "RPAREN", "LT", "GT", "EQ", "NEQ", "LE", "GE", "AND", "OR", "EOF"}:
            print("Regla: T_L → ε")
            return inherited
        else:
            raise SyntaxError(f"Token inesperado en T_L: {tok.type}")

    def parse_P(self):
        print("Regla: P → F P_L")
        left = self.parse_F()
        return self.parse_P_L(left)

    def parse_P_L(self, inherited):
        tok = self.current_token()
        if tok.type == "EXP":
            print("Regla: P_L → ^ F P_L")
            self.match("EXP")
            right = self.parse_F()
            result = inherited["valor"] ** right["valor"]
            return self.parse_P_L({"valor": result})

        elif tok.type in {"MUL", "DIV", "ADD", "SUB", "RPAREN", "LT", "GT", "EQ", "NEQ", "LE", "GE", "AND", "OR", "EOF"}:
            print("Regla: P_L → ε")
            return inherited
        else:
            raise SyntaxError(f"Token inesperado en P_L: {tok.type}")

    def parse_F(self):
        tok = self.current_token()
        if tok.type == "NUM":
            print("Regla: F → NUM")
            self.match("NUM")
            return {"valor": tok.value}

        elif tok.type == "LPAREN":
            print("Regla: F → ( ELO )")
            self.match("LPAREN")
            result = self.parse_ELO()
            self.match("RPAREN")
            return {"valor": result["valor"]}

        else:
            raise SyntaxError(f"Token inesperado en F: {tok.type}")
