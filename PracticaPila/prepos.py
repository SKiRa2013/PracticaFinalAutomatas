# Prefija: - + 84 / 12 ( + ^ 4 2 8 ) * 7 3
# Infija: 84 + 12 / ( 4 ^ 2 + 8 ) - 7 * 3
# Posfija: 84 12 ( 4 2 ^ 8 + ) / +  7 3 * -

def jerarquia_operacion(op):
    if op == '^':
        return 3
    
    elif op in '*/':
        return 2
    
    elif op in '+-':
        return 1
    
    return 0

def partir_valores(string: str):
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

def infija_a_prefija(str_list):
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
                   ((jerarquia_operacion(elem) < jerarquia_operacion(pila[-1])) or
                    (jerarquia_operacion(elem) == jerarquia_operacion(pila[-1]) and elem != '^'))):
                
                res_lista.append(pila.pop())
                
            pila.append(elem)

    while pila:
        res_lista.append(pila.pop())

    return res_lista

def posfija_a_prefija(string):
    pila = []

    for elem in string:
        if elem in '+-*/^':
            op1 = pila.pop()
            op2 = pila.pop()
            
            new_expr = elem + ' ' + op2 + ' ' + op1
            
            pila.append(new_expr)
            
        else:
            pila.append(elem)

    return pila[-1]

def conversion(string):
    str_list = partir_valores(string)
    
    postfix = infija_a_prefija(str_list)
    prefix = posfija_a_prefija(postfix)
    
    return [prefix, ' '.join(postfix)]


infija = "84+12/(4^2+8)-7*3"

conv = conversion(infija)
prefija = conv[0]
posfija = conv[1]

print(f"Prefija: {prefija}\nInfija: {infija}\nPosfija: {posfija}")