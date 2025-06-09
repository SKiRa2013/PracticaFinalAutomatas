import re

class ConversionExpr:
    def __init__(self, string: str):
        self.prefija: str
        self.infija: str = ""
        self.posfija: str 
        
        # Arreglar infija
        symbol_list = [st for st in string.replace("0", "").replace("1", "").replace("2", "").replace("3", "").replace("4", "").replace("5", "").replace("6", "").replace("7", "").replace("8", "").replace("9", "")]
        
        num = ""
        symbol_count = 0
        
        for char in string:
            if char in '+-*/^()':
                self.infija += f"{num} {symbol_list[symbol_count]} "
                
                num = ""
                symbol_count += 1
            else:
                num += char
        
        self.infija += f"{num}"
        
        self.infija = re.sub(r"\s+", " ", self.infija)        
        self.conversion_expr(string)
    
    def jerarquia_operacion(self, op):
        if op == '^':
            return 3
        
        elif op in '*/':
            return 2
        
        elif op in '+-':
            return 1
        
        return 0

    def partir_valores(self, string: str):
        str_list = []
        num = ""
        
        for char in string:
            if char.isdigit():
                num += char
                
            elif char in '+-*/^()':
                if num != "":
                    str_list.append(num)
                    num = ""
                
                str_list.append(char)
            elif char == " ":
                if num != "":
                    str_list.append(num)
                    num = ""
        
        if num != "":
            str_list.append(num)
            
        return str_list

    def infija_a_posfija(self, str_list) -> str:
        pila = []
        res_lista = []

        for elem in str_list:
            if elem.isdigit():
                res_lista.append(elem)
            
            elif elem == '(':
                pila.append(elem)
                
            elif elem == ')':
                while pila and pila[-1] != '(':
                    res_lista.append(pila.pop())
                    
                pila.pop()
                
            elif elem in '+-*/^':
                while (pila and pila[-1] in '+-*/^' and
                    ((self.jerarquia_operacion(elem) < self.jerarquia_operacion(pila[-1])) or
                        (self.jerarquia_operacion(elem) == self.jerarquia_operacion(pila[-1]) and elem != '^'))):
                    
                    res_lista.append(pila.pop())
                    
                pila.append(elem)

        while pila:
            res_lista.append(pila.pop())

        return ' '.join(res_lista)

    def posfija_a_prefija(self, str_list):
        pila = []

        for elem in str_list:
            if elem in '+-*/^':
                op1 = pila.pop()
                op2 = pila.pop()
                
                new_expr = elem + ' ' + op2 + ' ' + op1
                
                pila.append(new_expr)
                
            else:
                pila.append(elem)

        return "".join(pila[-1])

    def conversion_expr(self, string):
        str_list = self.partir_valores(string)
        
        postfix = self.infija_a_posfija(str_list).split()
        prefix = self.posfija_a_prefija(postfix)
        
        self.prefija = prefix
        self.posfija = " ".join(postfix)


if __name__ == "__main__":
    infija = "84+12/(4^2+8)-7*3"

    conv = ConversionExpr(infija)
    
    print(f"Prefija: {conv.prefija}\nInfija: {conv.infija}\nPosfija: {conv.posfija}")
    
    
84 + 12 /  ( 4 ^ 2 + 8 )  - 7 * 3