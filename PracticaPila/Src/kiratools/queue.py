class QueueNode:
    def __init__(self, node): 
        self.node = node
        self.next = None

class Queue:
    def __init__(self, name="Cola"):
        self.start = None
        self.end = None
        self.name = name

    def __str__(self):
        string = ""
        aux = self.start
        
        if aux is not None:
            while aux.next is not None:
                string += f"{aux.node}, "
                aux = aux.next
            
            string += f"{aux.node}"
        
        return string

    # Ingresar de último
    def enqueue_node(self, node):
        print(f"Agregar {node} en {self.name}")
        
        aux = QueueNode(node)
        
        if self.start is None:
            self.start = aux
    
        else:
            self.end.next = aux
    
        self.end = aux         
    
    # Sacar primero
    def dequeue_node(self) -> QueueNode:
        if self.start is None:
            print(f"No se puede sacar de {self.name}")
            return None

        aux = self.start

        print(f"Sale {self.start.node} en {self.name}")
        self.start = self.start.next
        
        return aux

    # Imprimir cola
    def print_queue(self):
        if self.start is None:
            print(f"No hay ningún elemento en {self.name}...")
            return
        
        print(f"Datos de {self.name}:")
        
        aux = self.start
        while aux is not None:
            print(f"{aux.node}", end="\n")
            aux = aux.next
    
    # Confirmar si está vacía la pila        
    def is_empty(self):
        return self.start is None


if __name__ == "__main__":
    op = -1
    cola = None

    while(op != 0):
        print("MENU Cola")
        print ("1. Inicializar Cola")
        print ("2. Ingresar dato")
        print ("3. Sacar dato")
        print ("4. Imprimir")
        print ("0. Salir")
        
        op = int(input("Digite su opción: "))
        
        match op:
            case 1:
                print('Inicializar')
                cola = Queue()

            case 2:
                if cola is None:
                    print(f"{cola.name} no se ha inicializado aún.")
                
                else:
                    print('Ingresar último')
                    dato = input("Dato: ")
                    cola.enqueue_node(dato)  
            
            case 3:
                if cola is None:
                    print(f"{cola.name} no se ha inicializado aún.")
                
                else:
                    cola.print_queue()
                    cola.dequeue_node()
                    cola.print_queue()

            case 4:
                if cola is None:
                    print(f"{cola.name} no se ha inicializado aún.")
                
                else:
                    print('Imprimir')
                    cola.print_queue()

            case 0:
                print('Salir')
