from logic import *

# Símbolos que representan el estado de los habitantes
ACaballero = Symbol('A es caballero')
ALadron = Symbol('A es ladron')
BCaballero = Symbol('B es caballero')
BLadron = Symbol('B es ladron')
CCaballero = Symbol('C es caballero')
CLadron = Symbol('C es ladron')
B_no_dijo_nada = Symbol('B no dijo nada')
B_dijo_A_ladron = Symbol('B dijo: A es ladron')
C_dijo_A_caballero = Symbol('C dijo: A es caballero')

# ESCENARIO 1
knowledge1 = And(
    Implication(ACaballero, And(ACaballero, ALadron)),  # A dice que es caballero y ladrón
)

# ESCENARIO 2
knowledge2 = And(
    Implication(ACaballero, And(ALadron, BCaballero)),  # A dice que ambos son ladrones, entonces A es ladrón y B es caballero, o viceversa
    B_no_dijo_nada,  # B no dice nada
    Or(And(ALadron, BCaballero), And(ACaballero, BLadron)),  # A y B son uno ladrón y uno caballero, o viceversa
)

# ESCENARIO 3
knowledge3 = And(
    Implication(ACaballero, Or(And(ACaballero, BCaballero), And(ALadron, BLadron))),  # A dice que son del mismo tipo
    Implication(ACaballero, Or(And(ACaballero, BLadron), And(ALadron, BCaballero))),  # A dice que son de distintos tipos
    Not(B_no_dijo_nada),  # B dice algo
    Not(And(ACaballero, BCaballero)),  # A y B no pueden ser iguales
    Not(And(ALadron, BLadron)),  # A y B no pueden ser ambos ladrones
)

# ESCENARIO 4
knowledge4 = And(
    Or(And(ACaballero, Not(B_dijo_A_ladron)), And(ALadron, B_dijo_A_ladron)),  # A dice que es caballero o ladrón (pero no sabemos cuál frase dijo)
    Implication(B_dijo_A_ladron, ALadron),  # Si B dice que A dijo "Soy un ladron", entonces A es ladron
    Implication(And(BLadron, B_dijo_A_ladron), CLadron),  # B luego dice que C es ladrón
    Implication(C_dijo_A_caballero, ACaballero),  # C dice que A es caballero
    Not(And(ACaballero, BCaballero)),  # A y B no pueden ser iguales
    Not(And(ACaballero, CCaballero)),  # A y C no pueden ser iguales
    Not(And(BCaballero, CCaballero)),  # B y C no pueden ser iguales
    Not(And(ALadron, CLadron)),  # A y C no pueden ser ambos ladrones
    Not(And(BLadron, CLadron)),  # B y C no pueden ser ambos ladrones
)

# Imprimir resultados
model = {}

# Escenario 1
model['A'] = 'caballero' if model_check(knowledge1, ACaballero) else 'ladron'
print("ESCENARIO 1:", model['A'])

# Escenario 2
model['A'] = 'caballero' if model_check(knowledge2, ACaballero) else 'ladron'
model['B'] = 'caballero' if model_check(knowledge2, BCaballero) else 'ladron'
print("ESCENARIO 2:", model['A'], "y", model['B'])

# Escenario 3
model['A'] = 'caballero' if model_check(knowledge3, ACaballero) else 'ladron'
model['B'] = 'caballero' if model_check(knowledge3, BCaballero) else 'ladron'
print("ESCENARIO 3:", model['A'], "y", model['B'])

# Escenario 4
model['A'] = 'caballero' if model_check(knowledge4, ACaballero) else 'ladron'
model['B'] = 'caballero' if model_check(knowledge4, BCaballero) else 'ladron'
model['C'] = 'caballero' if model_check(knowledge4, CCaballero) else 'ladron'
print("ESCENARIO 4:", model['A'], ",", model['B'], "y", model['C'])
