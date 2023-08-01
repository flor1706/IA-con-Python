from logic import *

# Símbolos que representan el estado de los habitantes
ACaballero = Symbol('A es caballero')
ALadron = Symbol('A es ladron')
BCaballero = Symbol('B es caballero')
BLadron = Symbol('B es ladron')
CCaballero = Symbol('C es caballero')
CLadron = Symbol('C es ladron')

# FUNCIONES AUXILIARES

# Función para verificar si A, B y C son distintos entre sí
def son_distintos(model):
    return model[ACaballero] != model[BCaballero] and model[ACaballero] != model[CCaballero] and model[BCaballero] != model[CCaballero]

# ESCENARIO 1
# Nuevas proposiciones lógicas para lo que A dice en el escenario 1
A_no_caballero_y_ladron = And(Not(ACaballero), ALadron)  # A dice que no es caballero y es ladrón
A_no_caballero_ni_ladron = And(Not(ACaballero), Not(ALadron))  # A dice que no es caballero ni ladrón
A_caballero = ACaballero  # A dice que es caballero

# Agregar las nuevas proposiciones lógicas al conjunto de conocimientos del escenario 1
knowledge1 = And(
    Implication(A_caballero, Not(A_no_caballero_y_ladron)),
    Implication(Not(A_caballero), Not(A_no_caballero_ni_ladron)),
    Implication(A_no_caballero_y_ladron, Not(ACaballero)),
    Implication(A_no_caballero_y_ladron, ALadron),
    Implication(A_no_caballero_ni_ladron, Not(ACaballero)),
    Implication(A_no_caballero_ni_ladron, Not(ALadron)),
    Implication(Not(ACaballero), ALadron),
    Or(ACaballero, ALadron),
    Not(And(ACaballero, ALadron)),
)

# Ahora, para imprimir si lo que dice A es verdadero o falso en el escenario 1:
model = {}
if model_check(knowledge1, A_caballero):
    print("ESCENARIO 1: A dice la verdad, es un caballero.")
else:
    print("ESCENARIO 1: A miente, es un ladrón.")


# ESCENARIO 2
# Nuevas proposiciones lógicas para lo que A y B dicen en el escenario 2
A_ambos_ladrones = And(ALadron, BLadron)  # A dice que ambos son ladrones
B_no_dice_nada = Not(Or(BCaballero, BLadron))  # B no dice nada
A_ladron_B_caballero = Or(And(ALadron, BCaballero), And(ACaballero, BLadron))  # A es ladrón y B es caballero, o viceversa

# Agregar las nuevas proposiciones lógicas al conjunto de conocimientos del escenario 2
knowledge2 = And(
    Implication(A_ambos_ladrones, Not(And(ACaballero, BCaballero))),  # Si A dice que ambos son ladrones, entonces A y B no pueden ser ambos caballeros
    Implication(A_ambos_ladrones, And(ALadron, BLadron)),  # Si A dice que ambos son ladrones, entonces A y B son ambos ladrones
    B_no_dice_nada,  # Agregar la proposición lógica de que B no dice nada
    A_ladron_B_caballero,  # Agregar la proposición lógica que asegura que A y B son uno ladrón y uno caballero
)

# Ahora, para imprimir si lo que dice A es verdadero o falso en el escenario 2:
model = {}
if model_check(knowledge2, A_ambos_ladrones):
    print("ESCENARIO 2: A dice la verdad, ambos son ladrones.")
else:
    print("ESCENARIO 2: A miente, no son ambos ladrones.")

 # Para imprimir si B es caballero o ladrón en el escenario 2:
model = {}
if model_check(knowledge2, BCaballero):
    print("ESCENARIO 2: B dice la verdad, es un caballero.")
else:
    print("ESCENARIO 2: B miente, es un ladrón.")  

 # Para imprimir si A y B son ladrón y caballero (uno cada uno) en el escenario 2:
model = {}
if model_check(knowledge2, A_ladron_B_caballero):
    print("ESCENARIO 2: A es ladrón y B es caballero.")
elif model_check(knowledge2, Not(A_ladron_B_caballero)):
    print("ESCENARIO 2: A es caballero y B es ladrón.")
else:
    print("ESCENARIO 2: No se puede determinar quién es ladrón y quién es caballero.")


# ESCENARIO 3
# Nuevas proposiciones lógicas para lo que A y B dicen en el escenario 3
A_mismo_tipo_B_distinto_tipo = And(Or(And(ACaballero, BCaballero), And(ALadron, BLadron)), Or(And(ACaballero, BLadron), And(ALadron, BCaballero)))  # A dice que son del mismo tipo, B dice que son de distintos tipos
A_ladron_B_caballero = Or(And(ALadron, BCaballero), And(ACaballero, BLadron))  # A es ladrón y B es caballero, o viceversa

# Agregar las nuevas proposiciones lógicas al conjunto de conocimientos del escenario 3
knowledge3 = And(
    A_mismo_tipo_B_distinto_tipo,  # Asegurar que lo que dice A es cierto y lo que dice B es cierto
    A_ladron_B_caballero,  # Agregar la proposición lógica que asegura que A y B son uno ladrón y uno caballero
)

# Ahora, para imprimir si lo que dice A y B es verdadero o falso en el escenario 3:
model = {}
if model_check(knowledge3, A_mismo_tipo_B_distinto_tipo):
    print("ESCENARIO 3: A dice la verdad, somos del mismo tipo. B dice la verdad, somos de distintos tipos.")
else:
    print("ESCENARIO 3: A miente, no somos del mismo tipo. B miente, no somos de distintos tipos.")

# Para imprimir quién es caballero y quién es ladrón en el escenario 3:
model = {}
if model_check(knowledge3, A_ladron_B_caballero):
    print("ESCENARIO 3: A es ladrón y B es caballero.")
elif model_check(knowledge3, Not(A_ladron_B_caballero)):
    print("ESCENARIO 3: A es caballero y B es ladrón.")
else:
    print("ESCENARIO 3: No se puede determinar quién es ladrón y quién es caballero.")


# ESCENARIO 4
# Nuevas proposiciones lógicas para lo que A, B y C dicen en el escenario 4
A_caballero_o_ladron = Or(ACaballero, ALadron)  # A dice que es caballero o ladrón (pero no sabemos cuál frase dijo)
B_dijo_A_ladron = Or(ACaballero, ALadron)  # B dice que A dijo "Soy un ladrón"
B_luego_dijo_C_ladron = Or(BCaballero, BLadron)  # B luego dice que C es un ladrón
C_dijo_A_caballero = Or(ACaballero, ALadron)  # C dice que A es un caballero

# Agregar las nuevas proposiciones lógicas al conjunto de conocimientos del escenario 4
knowledge4 = And(
    # Asegurar que lo que dice A es cierto
    Or(And(A_caballero_o_ladron, B_dijo_A_ladron), And(A_caballero_o_ladron, Not(B_dijo_A_ladron))),
    # Si B dice que A dijo "Soy un ladrón", entonces A es ladrón
    Implication(B_dijo_A_ladron, ALadron),
    # Si B luego dice que C es un ladrón, entonces C es ladrón
    Implication(B_luego_dijo_C_ladron, CLadron),
    # Si C dice que A es un caballero, entonces A es caballero
    Implication(C_dijo_A_caballero, ACaballero),
    # A no puede haber dicho las dos frases a la vez
    Not(And(A_caballero_o_ladron, B_dijo_A_ladron)),
    # A y C no pueden ser iguales
    Not(And(A_caballero_o_ladron, C_dijo_A_caballero)),
    # B no puede haber dicho las dos frases a la vez
    Not(And(B_dijo_A_ladron, B_luego_dijo_C_ladron)),
    # B y C no pueden ser iguales
    Not(And(B_dijo_A_ladron, C_dijo_A_caballero)),
    # C no puede haber dicho las dos frases a la vez
    Not(And(C_dijo_A_caballero, B_luego_dijo_C_ladron)),
    # A y B no pueden ser iguales
    Not(And(ACaballero, BCaballero)),
    # A y C no pueden ser iguales
    Not(And(ACaballero, CCaballero)),
    # B y C no pueden ser iguales
    Not(And(BCaballero, CCaballero)),
    # A, B y C no pueden ser los tres caballeros o los tres ladrones
    son_distintos,
)

# Ahora, para imprimir quién es ladrón y quién es caballero en el escenario 4:
model = {}

# Verificar el estado de A (caballero o ladrón)
if model_check(knowledge4, ACaballero):
    print("ESCENARIO 4: A es un caballero.")
else:
    print("ESCENARIO 4: A es un ladrón.")

# Verificar el estado de B (caballero o ladrón)
if model_check(knowledge4, BCaballero):
    print("ESCENARIO 4: B es un caballero.")
else:
    print("ESCENARIO 4: B es un ladrón.")

# Verificar el estado de C (caballero o ladrón)
if model_check(knowledge4, CCaballero):
    print("ESCENARIO 4: C es un caballero.")
else:
    print("ESCENARIO 4: C es un ladrón.")
