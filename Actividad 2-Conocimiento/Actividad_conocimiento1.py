from logic import *

# Símbolos que representan el estado de los habitantes
ACaballero = Symbol('A es caballero')
ALadron = Symbol('A es ladron')
BCaballero = Symbol('B es caballero')
BLadron = Symbol('B es ladron')
CCaballero = Symbol('C es caballero')
CLadron = Symbol('C es ladron')

# ESCENARIO 1
knowledge1 = And(
    Implication(ACaballero, And(ACaballero, ALadron)),  # A dice que es caballero y ladrón
)

# ESCENARIO 2
knowledge2 = And(
    Implication(ACaballero, And(ALadron, BCaballero)),  # A dice que ambos son ladrones, entonces A es ladrón y B es caballero, o viceversa
    Or(And(ALadron, BCaballero), And(ACaballero, BLadron)),  # A y B son uno ladrón y uno caballero, o viceversa
    Not(And(ACaballero, BCaballero)),  # A y B no pueden ser iguales
)

# ESCENARIO 3
knowledge3 = And(
    # A y B son de tipos distintos, entonces uno es ladrón y otro es caballero
    Or(And(ACaballero, Not(BCaballero)), And(Not(ACaballero), BCaballero)),
    # A dice que son del mismo tipo, entonces A y B deben ser iguales (ambos ladrones o ambos caballeros)
    Implication(ACaballero, BCaballero),
    Implication(ALadron, BLadron),
    # B dice que son de distintos tipos, entonces A y B deben ser diferentes (uno ladron y otro caballero)
    Implication(ACaballero, BLadron),
    Implication(ALadron, BCaballero),
    Not(And(ACaballero, BCaballero)),  # A y B no pueden ser iguales
    Not(And(ALadron, BLadron)),  # A y B no pueden ser ambos ladrones
)

# ESCENARIO 4
knowledge4 = And(
    Or(ACaballero, ALadron),  # A dice que es caballero o ladrón (pero no sabemos cuál frase dijo)
    Or(BCaballero,BLadron),
    Or(CCaballero,CLadron),
    Implication(ACaballero,Or(ACaballero, ALadron)),  # B dice que A dijo "Soy un ladrón"
    Implication(ALadron,Not(Or(ACaballero,ALadron))),
    Implication(BCaballero,And(ALadron, CLadron)),  # B luego dice que C es ladrón
    Implication(BLadron,Not(And(ALadron,CLadron))),  # C dice que A es caballero
    Implication(CCaballero,ACaballero),
    Implication(CLadron, Not(ACaballero)),
    Not(And(ACaballero, ALadron)),  # A no puede haber dicho las dos frases a la vez
    Not(And(BCaballero, BLadron)),  # B no puede haber dicho las dos frases a la vez
    Not(And(CCaballero,CLadron)),
)

# Imprimir resultados
model = {}

# Escenario 1
model['A'] = 'A es caballero' if model_check(knowledge1, ACaballero) else ' A es ladron'
print("ESCENARIO 1:", model['A'])

# Escenario 2
model['A'] = 'A es caballero' if model_check(knowledge2, ACaballero) else 'A es ladron'
model['B'] = 'B es caballero' if model_check(knowledge2, BCaballero) else 'B es ladron'
print("ESCENARIO 2:", model['A'], "y", model['B'])

# Escenario 3
model['A'] = 'A es caballero' if model_check(knowledge3, ACaballero) else 'A es ladron'
model['B'] = 'B es caballero' if model_check(knowledge3, BCaballero) else 'B es ladron'
print("ESCENARIO 3:", model['A'], "y", model['B'])

# Escenario 4
model['A'] = 'A es caballero' if model_check(knowledge4, ACaballero) else 'A es ladron'
model['B'] = 'B es caballero' if model_check(knowledge4, BCaballero) else 'B es ladron'
model['C'] = 'C es caballero' if model_check(knowledge4, CCaballero) else 'C es ladron'
print("ESCENARIO 4:", model['A'], ",", model['B'], "y", model['C'])
