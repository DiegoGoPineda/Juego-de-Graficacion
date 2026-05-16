# Actions/state.py
from Actions.colisiones import CollisionObject

class PlayerState:
    def __init__(self, x_inicial=0.0, nombre="Personaje", tipo="gato"):
        self.nombre = nombre
        self.tipo = tipo  
        self.x, self.y, self.z = x_inicial, 0.0, 0.0

        # variables colis pa toddos
        self.expression = "neutral"
        self.reaction_type = None
        self.reaction_timer = 0
        self.reaction_duration = 30
        self.walking = False
        self.animation_angle = 0.0
        self.leg_swing = 0.0
        self.direction_angle = 0.0  # Ángulo de rotación basado en dirección de movimiento
        
        # las que comparten los personajes
        self.moving_tail = False
        self.tail_angle = 0.0
        self.blinking = True
        self.blink_timer = 0.0
        
        # estas son del gato
        self.arm_waving = False
        self.arm_wave_angle = 0.0
        self.ears_twitching = False
        self.ears_twitch_angle = 0.0
        self.front_paws_up_active = False
        self.front_paws_up_angle = 0.0
        # colisiones
        self.hay_choque = False
        self.color_colision_actual = (1.0, 1.0, 1.0)
        # mejora de la luz 
        self.is_shadow_pass = False
        # salto y balanceo de paso
        self.is_jumping = False
        self.jump_velocity = 0.0
        self.jump_offset = 0.0
        self.walk_bob = 0.0
        self.arm_left_angle = 0.0
        self.arm_right_angle = 0.0
        self.lives = 5
        # Salto
        self.is_jumping = False
        self.jump_velocity = 0.0
        self.jump_offset = 0.0
        # Mejora de animación de brazos
        self.arm_left_angle = 0.0
        self.arm_right_angle = 0.0

# o pa menu, 1 y pa elegir y 2 pa jugar
MENU_PRINCIPAL = 0
MENU_SELECCION = 1
MENU_ESCENARIO = 3
EN_JUEGO = 2
MENU_PAUSA = 4
MENU_AYUDA = 5

# fases especiales del primer nivel
LEVEL1_NONE = 0
LEVEL1_WAITING = 1
LEVEL1_TRANSITION = 2
LEVEL1_COUNTDOWN = 3
LEVEL1_ACTIVE = 4
LEVEL1_TRIVIA = 5
LEVEL1_FINISHED = 6

# estado
estado_actual = MENU_PRINCIPAL # El juego ahora inicia en el Menú de botones
indice_boton = 0               # 0: Jugar, 1: Mundo libre, 2: Salir
en_menu_seleccion = False      # Se activará cuando se de a juar

# Modo de juego
modo_juego = 'niveles'  # 'niveles' o 'libre'
nivel_actual = 1  # Para modo niveles
# luz nueva
shading_mode = "Gouraud" # 
is_shadow_pass = False   # Variable global para el estado de la luz

indice_escenario = 0
indice_pausa = 0

escenarios_pool = [
    {"id": 1, "nombre": "Ciudad Futuro", "color": (0.1, 0.6, 1.0)},
    {"id": 2, "nombre": "Jardín Mágico", "color": (0.2, 0.8, 0.3)},
    {"id": 3, "nombre": "Cueva Misteriosa", "color": (0.8, 0.2, 0.8)},
    {"id": 4, "nombre": "Salón de Clases", "color": (0.5, 0.3, 0.1)},
    {"id": 5, "nombre": "Cancha de Fútbol", "color": (0.1, 0.5, 0.1)},
    {"id": 6, "nombre": "Auditorio de Graduaciones", "color": (0.6, 0.4, 0.2)},
    {"id": 7, "nombre": "Océano Profundo", "color": (0.0, 0.2, 0.4)}
]

niveles_pool = [
    {"id": 4, "nombre": "Nivel 1", "color": (0.5, 0.3, 0.1)},
    {"id": 5, "nombre": "Nivel 2", "color": (0.1, 0.5, 0.1)},
    {"id": 6, "nombre": "Nivel 3", "color": (0.6, 0.4, 0.2)}
]

pause_menu_options = [
    "Reanudar",
    "Volver al menú principal",
    "Volver a seleccionar personajes",
    "Ayuda"
]

# instancia de los 2 jugapapus
p1 = PlayerState(x_inicial=-99.0, nombre="P1", tipo="gato")
p2 = PlayerState(x_inicial=99.0, nombre="P2", tipo="lola")

# toods los pj que se pueden elegir en el menu de seleccion
personajes_pool = [
    PlayerState(nombre="Timoteo", tipo="gato"),
    PlayerState(nombre="Lola", tipo="lola"),
    PlayerState(nombre="Mosca", tipo="mosca"),
    # papuling
    PlayerState(nombre="King Li", tipo="KingLi"), 
    PlayerState(nombre="Among Us", tipo="amongus"),
    PlayerState(nombre="Meteoro", tipo="meteoro"),
]

# como se seleccionan 
fase_seleccion = 1  # 1: P1 eligiendo, 2: P2 eligiendo
indice_menu = 0    # Índice del personaje actualmente resaltado en el menú
# mundo papu
scenario = 1
sonido_activo = True
show_instructions = True
scene_bounds = {"x": (-35.0, 35.0), "z": (-35.0, 35.0)}  # Límites dinámicos según escenario

# Primer nivel: inicio en salón de clases con plataformas y trivia
level1_enabled = False
level1_phase = LEVEL1_NONE
level1_transition_alpha = 0.0
level1_countdown = 3
level1_countdown_timer = 0
level1_hazard_timer = 0
level1_play_timer = 0
level1_hazards = []
# Plataformas iniciales visibles junto al pizarrón: izquierda y derecha
level1_platforms = [(-26.0, -36.0, 8.0, 4.0), (26.0, -36.0, 8.0, 4.0)]
# Posiciones de espera antes de comenzar el nivel 1
level1_wait_positions = [(-10.0, -18.0), (10.0, -18.0)]
# Posiciones de inicio activo cuando arranca el juego
level1_active_positions = [(-12.0, -24.0), (12.0, -24.0)]
level1_message = ""
level1_current_question = None
level1_question_target = None  # 'p1' o 'p2'
level1_feedback = ""
level1_feedback_timer = 0
# Trivia state
level1_selected_option = 0  # 0, 1, 2 (A, B, C)
level1_trivia_answered = False
level1_show_feedback_msg = False  # Para mostrar Correcto/Incorrecto
level1_feedback_msg = ""
level1_feedback_msg_timer = 0
level1_game_over = False
level1_winner = None  # 'p1' o 'p2'
level1_loser = None
level1_trivia_questions = [
    {
        "pregunta": "¿En qué año se firmó originalmente el decreto de creación del Instituto Tecnológico de Toluca?",
        "opciones": ["1970", "1972", "1974"],
        "correct": 1
    },
    {
        "pregunta": "¿Cuál es la fecha exacta en la que el ITToluca inició formalmente sus actividades académicas?",
        "opciones": ["4 de septiembre de 1974", "1 de septiembre de 1972", "20 de noviembre de 1975"],
        "correct": 0
    },
    {
        "pregunta": "¿Con qué población inicial de estudiantes abrió sus puertas la institución en 1974?",
        "opciones": ["150 estudiantes", "400 estudiantes", "1,200 estudiantes"],
        "correct": 1
    },
    {
        "pregunta": "¿Cuál es la mascota oficial que representa el orgullo y la identidad del ITToluca?",
        "opciones": ["Los Potros", "Los Halcones", "Los Castores"],
        "correct": 1
    },
    {
        "pregunta": "Aunque lleva el nombre de la capital del estado (Toluca), ¿en qué municipio se ubican físicamente sus instalaciones actuales?",
        "opciones": ["Toluca", "Metepec", "Lerma"],
        "correct": 1
    },
    {
        "pregunta": "¿Cuál es el nombre de la gaceta informativa oficial de la comunidad del tecnológico?",
        "opciones": ["Xinan-Tec", "Tec-Toluca Al Día", "Voz Halcón"],
        "correct": 0
    },
    {
        "pregunta": "¿En qué año el plantel se integró formalmente al decreto presidencial del Tecnológico Nacional de México (TecNM)?",
        "opciones": ["2000", "2010", "2014"],
        "correct": 2
    },
    {
        "pregunta": "¿Qué nivel educativo adicional se incorporó a la oferta de la institución en agosto de 1979 para diversificar sus opciones técnicas?",
        "opciones": ["Bachillerato técnico", "Cursos de idiomas abiertos", "Doctorados en investigación"],
        "correct": 0
    },
    {
        "pregunta": "¿Con cuántos catedráticos o profesores fundadores inició actividades el instituto en sus primeras clases?",
        "opciones": ["25 catedráticos", "50 catedráticos", "100 catedráticos"],
        "correct": 1
    },
    {
        "pregunta": "¿Aproximadamente qué cantidad de alumnos alberga el ITToluca en la actualidad, consolidándose como un referente de ingeniería?",
        "opciones": ["Más de 1,500 estudiantes", "Más de 3,000 estudiantes", "Más de 5,800 estudiantes"],
        "correct": 2
    }
]

# Límites por escenario
scenario_bounds = {
    1: {"x": (-40.0, 40.0), "z": (-40.0, 40.0)},  # Ciudad futuro
    2: {"x": (-40.0, 40.0), "z": (-40.0, 40.0)},  # Jardín
    3: {"x": (-40.0, 40.0), "z": (-40.0, 40.0)},  # Cueva
    4: {"x": (-35.0, 35.0), "z": (-35.0, 35.0)},  # Salón de clases
    5: {"x": (-35.0, 35.0), "z": (-35.0, 35.0)},  # Cancha de fútbol
    6: {"x": (-35.0, 35.0), "z": (-35.0, 35.0)},  # Auditorio
    7: {"x": (-40.0, 40.0), "z": (-40.0, 40.0)}   # Océano
}

# Teclas presionadas (para movimiento simultáneo)
keys_pressed = {
    b'w': False, b'a': False, b's': False, b'd': False,
    'up': False, 'down': False, 'left': False, 'right': False
}

mouse_down = False
last_mouse_x = 0
last_mouse_y = 0

# Objetos de colisión (solo para escenarios libres 1, 2, 3, 7)
objetos_escenas = [
    CollisionObject(5.0, 5.0, 1.5, (0.6, 0.3, 0.1), "Caja", "surprised", "jump", "surprised"),
    CollisionObject(-5.0, -8.0, 1.0, (0.4, 0.4, 0.4), "Piedra", "angry", "shake", "angry"),
    CollisionObject(0.0, -12.0, 1.2, (0.1, 0.4, 0.1), "Arbusto", "interest", "spin", "interest"),
    CollisionObject(10.0, -5.0, 2.0, (0.3, 0.3, 0.7), "Contenedor", "fear", "shake", "fear"),
    CollisionObject(-10.0, 10.0, 0.8, (0.8, 0.2, 0.2), "Poste", "happy", "jump", "happy"),
    CollisionObject(0.0, -10.0, 1.2, (0.2, 0.8, 1.0), "Trampolin", "surprised", "jump"),
    CollisionObject(-10.0, 0.0, 1.0, (0.9, 0.1, 0.5), "Fruta Magica", "happy", "grow"),
    CollisionObject(10.0, -5.0, 0.8, (0.5, 0.0, 0.8), "Cristal Velocidad", "shouting", "flip")
]

# Objetos de colisión para Salón de Clases (escenario 4)
objetos_salon = [
    CollisionObject(-39, 0, 2.0, (0.86, 0.86, 0.78), "ParedIzq", None, None, width=2.0, depth=80.0),
    CollisionObject(39, 0, 2.0, (0.86, 0.86, 0.78), "ParedDer", None, None, width=2.0, depth=80.0),
    CollisionObject(0, -39, 2.0, (0.86, 0.86, 0.78), "ParedTrasera", None, None, width=80.0, depth=2.0),
    CollisionObject(0, 39, 2.0, (0.86, 0.86, 0.78), "ParedFrontal", None, None, width=80.0, depth=2.0),
    CollisionObject(0, -39, 2.0, (0.05, 0.05, 0.05), "Pizarron", None, None, width=40.0, depth=1.0),
    CollisionObject(0, -28, 2.0, (0.45, 0.3, 0.15), "Escritorio", None, None, width=12.0, depth=4.0),
]
for fila in range(4):
    for col in range(4):
        x = -28 + col * 16 + 4
        z = -10 + fila * 10 + 2.5
        objetos_salon.append(CollisionObject(x, z, 2.0, (0.55, 0.35, 0.18), f"Mesa{fila*4+col+1}", None, None, width=8.0, depth=5.0))

objetos_salon_level1_active = [
    CollisionObject(-39, 0, 2.0, (0.86, 0.86, 0.78), "ParedIzq", None, None, width=2.0, depth=80.0),
    CollisionObject(39, 0, 2.0, (0.86, 0.86, 0.78), "ParedDer", None, None, width=2.0, depth=80.0),
    CollisionObject(0, -39, 2.0, (0.86, 0.86, 0.78), "ParedTrasera", None, None, width=80.0, depth=2.0),
    CollisionObject(0, 39, 2.0, (0.86, 0.86, 0.78), "ParedFrontal", None, None, width=80.0, depth=2.0),
    CollisionObject(0, -39.5, 2.0, (0.05, 0.05, 0.05), "Pizarron", None, None, width=40.0, depth=1.0),
]

# Objetos de colisión para Cancha de Fútbol (escenario 5)
objetos_cancha = [
    CollisionObject(-39, 0, 2.0, (1, 1, 1), "LateralIzq", None, None, width=2.0, depth=40.0),
    CollisionObject(39, 0, 2.0, (1, 1, 1), "LateralDer", None, None, width=2.0, depth=40.0),
    CollisionObject(0, -19, 2.0, (1, 1, 1), "FondoInf", None, None, width=80.0, depth=2.0),
    CollisionObject(0, 19, 2.0, (1, 1, 1), "FondoSup", None, None, width=80.0, depth=2.0),
    CollisionObject(-35, 0, 2.0, (1, 1, 1), "Porteria1", None, None, width=2.0, depth=6.0),
    CollisionObject(35, 0, 2.0, (1, 1, 1), "Porteria2", None, None, width=2.0, depth=6.0),
    CollisionObject(0, 23.5, 2.0, (0.4, 0.4, 0.4), "GradasSup", None, None, width=70.0, depth=2.0),
    CollisionObject(0, -23.5, 2.0, (0.4, 0.4, 0.4), "GradasInf", None, None, width=70.0, depth=2.0),
]

# Objetos de colisión para Auditorio (escenario 6)
objetos_auditorio = [
    CollisionObject(0, -45, 2.5, (0.3, 0.2, 0.15), "Escenario", None, None, width=40.0, depth=10.0),
    CollisionObject(0, -5, 1.5, (0.55, 0.1, 0.1), "PasilloCentral", None, None, width=16.0, depth=10.0),
]
for fila in range(8):
    z = 2 + fila * 4 + 1.0
    for col in range(-8, 9, 4):
        objetos_auditorio.append(CollisionObject(col + 1.5, z, 1.5, (0.25, 0.25, 0.3), f"Asiento_{fila+1}_{(col+9)//4+1}", None, None, width=3.0, depth=2.0))
