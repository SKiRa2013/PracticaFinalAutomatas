class StackNode:
    def __init__(self, node): 
        self.node = node
        self.upper: StackNode | None = None
        self.lower: StackNode | None = None

class Stack:
    def __init__(self, name="Pila"):
        self.bottom: StackNode | None = None
        self.top: StackNode | None = None
        self.name = name
        
    def __str__(self):
        string = ""
        aux = self.bottom
        
        if aux is not None:
            while aux.upper is not None:
                string += f"{aux.node}, "
                aux = aux.upper
            
            string += f"{aux.node}"
        
        return string
            
    # Ingresar de último
    def push_node(self, node):
        print(f"Agregar {node} en {self.name}")
        
        new_node = StackNode(node)

        if self.bottom is None:
            self.bottom = new_node
            self.top = new_node
            return
        
        aux = self.bottom
        
        while aux.upper is not None:
            aux = aux.upper
        
        new_node.lower = aux    
        aux.upper = new_node
        aux = aux.upper
        self.top = aux         

    # Sacar último
    def pop_node(self) -> StackNode:
        if self.bottom is None:
            print(f"No se puede sacar de {self.name}")
            return None
        
        aux = self.bottom
             
        if self.bottom.upper is None:
            print(f"Sale {self.bottom.node} en {self.name}")
            self.bottom = None
            self.top = None            
            return aux

        prev = None
        
        while aux.upper is not None:
            prev = aux
            aux = aux.upper

        print(f"Sale {aux.node} en {self.name}")
        
        prev.upper = None
        self.top = prev
        return aux

    # Imprimir pila
    def print_stack(self):
        if self.bottom is None:
            print(f"No hay ningún elemento en {self.name}...")
            return
        
        print(f"Datos de {self.name}:")
        
        aux = self.bottom
        while aux is not None:
            print(f"{aux.node}", end="\n")
            aux = aux.upper
            
    # Fondo de pila
    def is_empty(self):
        return self.bottom is None

if __name__ == "__main__":
    op = -1
    pila = None

    while(op != 0):
        print("MENU Pila")
        print ("1. Inicializar Pila")
        print ("2. Ingresar dato")
        print ("3. Sacar dato")
        print ("4. Imprimir")
        print ("0. Salir")
        
        op = int(input("Digite su opción: "))
        
        match op:
            case 1:
                print('Inicializar')
                pila = Stack()

            case 2:
                if pila is None:
                    print(f"{pila.name} no se ha inicializado aún.")
                
                else:
                    print('Ingresar primero')
                    dato = input("Dato: ")
                    pila.push_node(dato)

            case 3:
                if pila is None:
                    print(f"{pila.name} no se ha inicializado aún.")
                
                else:
                    pila.print_stack()        
                    pila.pop_node()
                    pila.print_stack()

            case 4:
                if pila is None:
                    print(f"{pila.name} no se ha inicializado aún.")
                
                else:
                    print('Imprimir')
                    pila.print_stack()

            case 0:
                print('Salir')
