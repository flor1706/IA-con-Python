from colorama import  init,Fore,Back,Style

init()

class Nodo():

    def __init__(self,_estado,_padre, _costo_acumulado=0):#,_accion):
        self.estado=_estado   #Entendemos por estado (fila,columna)
        self.padre=_padre     
        #self.accion=_accion   #Accion es simplemente un texto
        #que diga que accion se realizo, ejemplo (Arriba,Abajo,Izquierda,Derecha)
        #No es fundamental para el funcionamiento
        self.costo_acumulado =_costo_acumulado  

class FronteraStack():

    def __init__(self):

        self.frontera=[]

    def __str__(self):

        return "Nodos en la frontera: " + " ".join(
            str(nodo.estado) for nodo in self.frontera)
    
    def agregar_nodo(self,_nodo):
        #Agregar el nodo pasado por parametro a la frontera
        self.frontera.append(_nodo)

    def quitar_nodo(self):
        #Quitar nodo de la frontera (respetar el tipo de frontera)
        return self.frontera.pop()
    
    def esta_vacia(self):
        #Comprobar si la frontera está vacia o no
        return len(self.frontera)==0
    
    def contiene_estado(self,_estado):
        #Comprobar si el estado pasado por parametro ya se encuentra en la frontera
        for nodo in self.frontera:

            if nodo.estado == _estado:
                return True
        return False


class FronteraQueue(FronteraStack):
    '''Aplicar herencia con FronteraStack
       La unica diferencia entre ambas es como
       se quitan los nodos
    '''
    def quitar_nodo(self):

        return self.frontera.pop(0)

class FronteraGreedy(FronteraStack):
    def distancia_manhattan(self, estado1, estado2):
        #la funcion distancia_manhattan calcula la distancia de Manhattan entre dos estados
        # es una funcion heuristica utilizada en el algoritmo greedy para evaluar la distancia entre el estado actual y la meta 
        fila1, columna1 = estado1
        fila2, columna2 = estado2
        return abs(fila1 - fila2) + abs(columna1 - columna2)
    
    def agregar_nodo(self, _nodo):
        #la funcion agregar_nodo agrega el nodo a la frontera greedy
        # antes de arreglarlo,calcula la priridad del nodo utilizando la heuristica distancia_manhattan
        #para estimar cuan cerca esta el estado actual de la meta
        if not hasattr(self,'meta'):
            raise ValueError('la meta no ha sido definida en la frontera Greedy')
        _nodo.prioridad = self.distancia_manhattan(_nodo.estado, self.meta)
        self.frontera.append(_nodo)

    def quitar_nodo(self):
        #la funcion se encarga de quitar el nodo con la menor prioridad de la frontera greedy
        #en este caso la prioridad esta dada por la distancia de manhattan calculada previamente en agragar nodo
        min_prioridad = float('inf')
        min_index = 0
        for i, nodo in enumerate(self.frontera):
            if nodo.prioridad < min_prioridad:
                min_prioridad = nodo.prioridad
                min_index = i
        return self.frontera.pop(min_index) 
    
class FronteraAStar(FronteraGreedy):
    def distancia_manhattan(self, estado1, estado2):
        fila1, columna1 = estado1
        fila2, columna2 = estado2
        return abs(fila1 - fila2) + abs(columna1 - columna2)

    def agregar_nodo(self, _nodo):
        #la funcion agrega el nodo a la frontera a*
        #antes de agregarlo calcula la prioridad del nodo utilizando la heuristica distancia_manhattan
        #y el costo acumulado desde el inicio hasta el estado actual(_nodo.costo_acumulado)
        #la prioridad se define como la suma del costo acumulado y la distancia de manhattan al estado objetivo(meta)
        if not hasattr(self, 'meta'):
            raise ValueError('La meta no ha sido definida en la frontera A*')
        _nodo.prioridad = _nodo.costo_acumulado + self.distancia_manhattan(_nodo.estado, self.meta)
        self.frontera.append(_nodo)   

class Laberinto():

    def  __init__(self,_algoritmo):
        '''Dentro del init podemos ejecutar funciones
           para ir definiendo los atributos de la clase.
           Les dejo lista la parte de leer el laberinto
           del archivo de texto, y la detección del inicio,
           meta y paredes.
        '''
        with open('laberinto.txt','r') as archivo:
            laberinto = archivo.read()     #Con read() leemos todo el archivo y lo guardamos en laberinto
        laberinto=laberinto.splitlines() #Con splitlines() separamos el laberinto en lineas, eliminando el \n
        self.ancho=len(laberinto[0])    #El ancho del laberinto es la cantidad 
                                        #de caracteres de la primer linea 
                                        #(O de cualquiera suponiendo que todas tienen el mismo ancho)
        self.alto=len(laberinto)        #El alto del laberinto es la cantidad de lineas
        self.paredes=[]                 #Lista de paredes

        for fila in range(self.alto):   #Recorremos todas las filas
            fila_paredes=[]             #Creamos una lista vacia para las paredes de la fila actual
                                        #para cada fila se vuelve a limpiar la lista
            for columna in range(self.ancho): #Recorremos todas las columnas
                if laberinto[fila][columna] == ' ': #Si el caracter es # es una pared
                    fila_paredes.append(False) #Agregamos la pared a la lista de paredes de la fila actual
                elif laberinto[fila][columna] == 'I':   #Si el caracter es I es el inicio
                    self.inicio = (fila,columna)
                    fila_paredes.append(False)         #Guardamos el inicio
                elif laberinto[fila][columna] == 'M':   #Si el caracter es M es la meta
                    self.meta = (fila,columna) 
                    fila_paredes.append(False)           #Guardamos la meta
                else:
                    fila_paredes.append(True) 
            self.paredes.append(fila_paredes)         #Agregamos la lista de paredes de la fila actual a la lista de paredes
        #De este modo ya tenemos identificadas las paredes, el inicio y la meta
        self.solucion = None
        self.algoritmo = _algoritmo #String en el que pasamos el nombre del algoritmo a utilizar


    def expandir_nodo(self,_nodo, frontera):
        '''Dentro de _nodo.estado tenemos la posicion actual del nodo
           Debemos comprobar en todas las direcciones si podemos movernos
           descartando las que sean paredes o esten fuera del laberinto                            (fila_a - 1, colum_a)
           Utilicen el grafico que está en el Notion para guiarse                (fila_a,colum_a-1) (fila_a, colum_a) (fila_a,colum_a+1)
           Devolver una lista de vecinos posibles (nodos hijo)                                     (fila_a + 1, colum_a)
        '''
        #        (0,2)
        #   (1,1)(1,2)(1,3)
        #        (2,2)
        # Nodo(estado:(fila,columna),padre:Nodo)
        fila_a , colum_a = _nodo.estado
        arriba = (fila_a -1, colum_a)
        izquierda = (fila_a , colum_a -1)
        abajo = (fila_a + 1, colum_a)
        derecha = (fila_a , colum_a +1)
        posiciones = [arriba,izquierda,abajo,derecha]
        vecinos = []
        for f,c in posiciones:
            if 0 <= f < self.alto and 0 <= c < self.ancho and not self.paredes[f][c]:
                vecinos.append((f,c))
        
        for vecino in vecinos:
            if not frontera.contiene_estado(vecino) and vecino not in self.nodos_explorados:
                nuevo_costo_acumulado = _nodo.costo_acumulado + 1  #costo acumulado del vecino es 1 mas que el del nodo actual
                nuevo_nodo = Nodo(vecino, _nodo, nuevo_costo_acumulado)
                frontera.agregar_nodo(nuevo_nodo)

        return vecinos
    
    def resolver(self):
        '''
        Acá tienen que implementar el algoritmo de busqueda
        La idea es intentar replicar el pseudocodigo que vimos en clase
        1- Inicializar la frontera con el nodo inicial
        2- Inicializar el conjunto de explorados como vacio
        3- Repetimos:
            3.1- Si la frontera esta vacia, no hay solucion
            3.2- Quitamos un nodo de la frontera
            3.3- Si el nodo contiene un estado que es meta, devolver la solucion
            3.4- Agregar el nodo a explorados
            3.5- Expandir el nodo, agregando los nodos hijos a la frontera
        '''
        if self.algoritmo=='BFS':
            #Crear la frontera que corresponda
            frontera = FronteraQueue()
        elif self.algoritmo=='DFS':
            #Crear la frontera que corresponda
            frontera = FronteraStack()
        elif self.algoritmo == 'Greedy':
            frontera = FronteraGreedy()
            frontera.meta = self.meta
        elif self.algoritmo == 'AStar':
            frontera =FronteraAStar()
            frontera.meta = self.meta
        #------------------------------------------------------------------------
        nodo_inicial = Nodo(self.inicio,None)
        frontera.agregar_nodo(nodo_inicial)
        self.nodos_explorados = []
        while True:
            if frontera.esta_vacia():
                raise Exception("No hay solucion")
            
            nodo_actual = frontera.quitar_nodo()
            if nodo_actual.estado == self.meta:
                #se encontro la meta.construir el camino
                camino=[nodo_actual.estado]
                padre= nodo_actual.padre
                while padre is  not None:
                    camino.append(padre.estado)
                    padre=padre.padre

                camino.reverse()
                self.solucion= camino
                
                print("Encontré la meta")
                return
                
            
            self.nodos_explorados.append(nodo_actual.estado)
            vecinos = self.expandir_nodo(nodo_actual, frontera)
            for vecino in vecinos:
                if not frontera.contiene_estado(vecino) and vecino not in self.nodos_explorados:
                    nuevo_nodo = Nodo(vecino,nodo_actual)
                    frontera.agregar_nodo(nuevo_nodo)

    def imprimir_laberinto(self):# INSTALAR COLORAMA EN LAS EXTENSIONES PARA QUE MUESTRE EL LABERINTO EN COLORES
        costo_total = 0
        for fila in range(self.alto):
            for columna in range(self.ancho):
                if self.paredes[fila][columna]:
                    print(Back.GREEN + ' ', end='')#imprime los espacios de pared en verde
                elif (fila,columna) in self.solucion:
                    print(Back.RED + ' ' , end='')#resalta el camino en rojo    
                    costo_total += 1 #cuenta el numero de nodos explorados
                else:
                    print(Back.WHITE + ' ', end='')#imprime los espacios vacios en blanco

            print(Back.RESET)

        print(f"Nodos Explorados: {len(self.nodos_explorados)}")

        print(f"Costo Total: {costo_total}")    
                          
       

laberinto = Laberinto('BFS')

laberinto.resolver()

laberinto.imprimir_laberinto()