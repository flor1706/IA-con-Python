from colorama import  init,Fore,Back,Style

init()

class Nodo():

    def __init__(self,_estado,_padre):#,_accion):
        self.estado=_estado   #Entendemos por estado (fila,columna)
        self.padre=_padre     
        #self.accion=_accion   #Accion es simplemente un texto
                              #que diga que accion se realizo, ejemplo (Arriba,Abajo,Izquierda,Derecha)
                              #No es fundamental para el funcionamiento
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

    def expandir_nodo(self,_nodo):
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
            vecinos = self.expandir_nodo(nodo_actual)
            for vecino in vecinos:
                if not frontera.contiene_estado(vecino) and vecino not in self.nodos_explorados:
                    nuevo_nodo = Nodo(vecino,nodo_actual)
                    frontera.agregar_nodo(nuevo_nodo)

    def imprimir_laberinto(self):
        for fila in range(self.alto):
            for columna in range(self.ancho):
                if self.paredes[fila][columna]:
                    print(Back.BLACK + ' ', end='')
                else:
                    print(Back.WHITE + ' ', end='')
            print(Back.RESET)                        

laberinto = Laberinto("BFS")
laberinto.imprimir_laberinto()
laberinto.resolver()