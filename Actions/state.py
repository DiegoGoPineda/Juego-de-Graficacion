# Actions/state.py
from Actions.colisiones import CollisionObject

class PlayerState:
    def __init__(self, x_inicial=0.0, nombre="Personaje", tipo="gato"):
        self.nombre = nombre
        self.tipo = tipo  
        self.x, self.y, self.z = x_inicial, 0.0, 0.0

        # Variables de colisión y reacciones para todos
        self.expression = "neutral"
        self.reaction_type = None
        self.reaction_timer = 0
        self.reaction_duration = 30
        self.walking = False
        self.animation_angle = 0.0
        self.leg_swing = 0.0
        self.direction_angle = 0.0  # Ángulo de rotación basado en dirección de movimiento
        
        # Variables compartidas por los personajes
        self.moving_tail = False
        self.tail_angle = 0.0
        self.blinking = True
        self.blink_timer = 0.0
        
        # Variables específicas del gato / animaciones avanzadas
        self.arm_waving = False
        self.arm_wave_angle = 0.0
        self.ears_twitching = False
        self.ears_twitch_angle = 0.0
        self.front_paws_up_active = False
        self.front_paws_up_angle = 0.0
        
        # Estado de colisiones en el frame actual
        self.hay_choque = False
        self.color_colision_actual = (1.0, 1.0, 1.0)
        
        # Renderizado y efectos
        self.is_shadow_pass = False
        self.walk_bob = 0.0
        self.lives = 5
        
        # Física de Salto (Limpiado y sin duplicados)
        self.is_jumping = False
        self.jump_velocity = 0.0
        self.jump_offset = 0.0
        
        # Animación de brazos (Limpiado y sin duplicados)
        self.arm_left_angle = 0.0
        self.arm_right_angle = 0.0

# --- ESTADOS DEL FLUJO PRINCIPAL ---
MENU_PRINCIPAL = 0
MENU_SELECCION = 1
MENU_ESCENARIO = 3
EN_JUEGO = 2
MENU_PAUSA = 4
MENU_AYUDA = 5

# --- FASES ESPECÍFICAS: NIVEL 1 (TRIVIA) ---
LEVEL1_NONE = 0
LEVEL1_WAITING = 1
LEVEL1_TRANSITION = 2
LEVEL1_COUNTDOWN = 3
LEVEL1_ACTIVE = 4
LEVEL1_TRIVIA = 5
LEVEL1_FINISHED = 6

# --- FASES ESPECÍFICAS: NIVEL 2 (FÚTBOL / BALONES) ---
LEVEL2_NONE = 0
LEVEL2_WAITING = 1   # Sala de espera / espera previa al inicio
LEVEL2_TRANSITION = 2  # Pantalla de carga / fundido al iniciar
LEVEL2_COUNTDOWN = 3   # Cuenta regresiva antes de jugar
LEVEL2_ACTIVE = 4      # Jugando, esquivando y disparando
LEVEL2_FINISHED = 5    # Fin del nivel (Pantalla de victoria)

# --- VARIABLES DE CONTROL GLOBAL ---
estado_actual = MENU_PRINCIPAL 
indice_boton = 0               # 0: Jugar, 1: Mundo libre, 2: Salir
en_menu_seleccion = False      # Se activa al dar a Jugar
modo_juego = 'niveles'         # 'niveles' o 'libre'
nivel_actual = 1               # Control de la campaña institucional

# Gráficos e Iluminación
shading_mode = "Gouraud" 
is_shadow_pass = False   

# Navegación de menús secundarios
indice_escenario = 0
indice_pausa = 0
fase_seleccion = 1             # 1: P1 eligiendo, 2: P2 eligiendo
indice_menu = 0                # Personaje resaltado
scenario = 1
sonido_activo = True
show_instructions = True

# --- CONFIGURACIÓN DE POOLS Y ENTIDADES ---

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

# Instancias de los jugadores de la partida
p1 = PlayerState(x_inicial=-99.0, nombre="P1", tipo="gato")
p2 = PlayerState(x_inicial=99.0, nombre="P2", tipo="lola")

# Personajes disponibles en el menú de selección
personajes_pool = [
    PlayerState(nombre="Timoteo", tipo="gato"),
    PlayerState(nombre="Lola", tipo="lola"),
    PlayerState(nombre="Mosca", tipo="mosca"),
    PlayerState(nombre="King Li", tipo="KingLi"), 
    PlayerState(nombre="Among Us", tipo="amongus"),
    PlayerState(nombre="Meteoro", tipo="meteoro"),
]

# --- LÍMITES DE ESCENARIOS ---
scenario_bounds = {
    1: {"x": (-40.0, 40.0), "z": (-40.0, 40.0)},
    2: {"x": (-40.0, 40.0), "z": (-40.0, 40.0)},
    3: {"x": (-40.0, 40.0), "z": (-40.0, 40.0)},
    4: {"x": (-35.0, 35.0), "z": (-35.0, 35.0)},  # Salón de clases
    5: {"x": (-35.0, 35.0), "z": (-35.0, 35.0)},  # Cancha de fútbol
    6: {"x": (-35.0, 35.0), "z": (-35.0, 35.0)},  # Auditorio
    7: {"x": (-40.0, 40.0), "z": (-40.0, 40.0)}
}

# Entrada de teclado (Movimiento simultáneo)
keys_pressed = {
    b'w': False, b'a': False, b's': False, b'd': False,
    'up': False, 'down': False, 'left': False, 'right': False
}

mouse_down = False
last_mouse_x = 0
last_mouse_y = 0

# --- CONFIGURACIÓN DE LOGÍSTICA: NIVEL 1 ---
level1_enabled = False
level1_phase = LEVEL1_NONE
level1_transition_alpha = 0.0
level1_countdown = 3
level1_countdown_timer = 0
level1_hazard_timer = 0
level1_play_timer = 0
level1_hazards = []
level1_platforms = [(-26.0, -36.0, 8.0, 4.0), (26.0, -36.0, 8.0, 4.0)]
level1_wait_positions = [(-10.0, -18.0), (10.0, -18.0)]
level1_active_positions = [(-12.0, -24.0), (12.0, -24.0)]
level1_message = ""
level1_current_question = None
level1_question_target = None  # 'p1' o 'p2'
level1_feedback = ""
level1_feedback_timer = 0
level1_selected_option = 0     # 0 (A), 1 (B), 2 (C)
level1_trivia_answered = False
level1_show_feedback_msg = False 
level1_feedback_msg = ""
level1_feedback_msg_timer = 0
level1_game_over = False
level1_winner = None           # 'p1' o 'p2'
level1_loser = None

level1_trivia_questions = [
    {"pregunta": "¿En qué año se firmó originalmente el decreto de creación del Instituto Tecnológico de Toluca?", "opciones": ["1970", "1972", "1974"], "correct": 1},
    {"pregunta": "¿Cuál es la fecha exacta en la que el ITToluca inició formalmente sus actividades académicas?", "opciones": ["4 de septiembre de 1974", "1 de septiembre de 1972", "20 de noviembre de 1975"], "correct": 0},
    {"pregunta": "¿Con qué población inicial de estudiantes abrió sus puertas la institución en 1974?", "opciones": ["150 estudiantes", "400 estudiantes", "1,200 estudiantes"], "correct": 1},
    {"pregunta": "¿Cuál es la mascota oficial que representa el orgullo y la identidad del ITToluca?", "opciones": ["Los Potros", "Los Halcones", "Los Castores"], "correct": 1},
    {"pregunta": "Aunque lleva el nombre de la capital del estado (Toluca), ¿en qué municipio se ubican físicamente sus instalaciones actuales?", "opciones": ["Toluca", "Metepec", "Lerma"], "correct": 1},
    {"pregunta": "¿Cuál es el nombre de la gaceta informativa oficial de la comunidad del tecnológico?", "opciones": ["Xinan-Tec", "Tec-Toluca Al Día", "Voz Halcón"], "correct": 0},
    {"pregunta": "¿En qué año el plantel se integró formalmente al decreto presidencial del Tecnológico Nacional de México (TecNM)?", "opciones": ["2000", "2010", "2014"], "correct": 2},
    {"pregunta": "¿Qué nivel educativo adicional se incorporó a la oferta de la institución en agosto de 1979 para diversificar sus opciones técnicas?", "opciones": ["Bachillerato técnico", "Cursos de idiomas abiertos", "Doctorados en investigación"], "correct": 0},
    {"pregunta": "¿Con cuántos catedráticos o profesores fundadores inició actividades el instituto en sus primeras clases?", "opciones": ["25 catedráticos", "50 catedráticos", "100 catedráticos"], "correct": 1},
    {"pregunta": "¿Aproximadamente qué cantidad de alumnos alberga el ITToluca en la actualidad, consolidándose como un referente de ingeniería?", "opciones": ["Más de 1,500 estudiantes", "Más de 3,000 estudiantes", "Más de 5,800 estudiantes"], "correct": 2}
]

# --- ESTRUCTURAS DE OBJETOS DE COLISIÓN ---
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

objetos_auditorio = [
    CollisionObject(0, -45, 2.5, (0.3, 0.2, 0.15), "Escenario", None, None, width=40.0, depth=10.0),
    CollisionObject(0, -5, 1.5, (0.55, 0.1, 0.1), "PasilloCentral", None, None, width=16.0, depth=10.0),
]
for fila in range(8):
    z = 2 + fila * 4 + 1.0
    for col in range(-8, 9, 4):
        objetos_auditorio.append(CollisionObject(col + 1.5, z, 1.5, (0.25, 0.25, 0.3), f"Asiento_{fila+1}_{(col+9)//4+1}", None, None, width=3.0, depth=2.0))


# =========================================================================
# --- NUEVAS VARIABLES DE CONFIGURACIÓN Y ESTADO PARA EL NIVEL 2 ---
# =========================================================================

level2_phase = LEVEL2_NONE
level2_timer = 0
level2_score_p1 = 0
level2_score_p2 = 0
level2_winning_score = 5
level2_transition_alpha = 0.0
level2_countdown = 3
level2_countdown_timer = 0
level2_message = "CARGANDO NIVEL 2..."

# Control del sistema de proyectiles (Cada elemento puede ser representado como un Cubo)
level_balones_enabled = True       
level_balones_jugador = []         # Estructura de diccionario: {"x": f, "z": f, "vx": f, "vz": f, "size": f, "owner": "p1"/"p2"}
level_balones_spawn_timer = 0

# Mecánicas competitivas y de balanceo
level2_cooldown_p1 = 0             # Temporizador interno para enfriamiento de disparo de P1
level2_cooldown_p2 = 0             # Temporizador interno para enfriamiento de disparo de P2
level2_cooldown_max = 25           # Cuadros/Frames obligatorios entre lanzamientos
level2_spawn_rate = 30             # Intervalo base para spawn automático de balones obstáculo
level2_ball_speed_multiplier = 1.0 # Escalabilidad de dificultad en tiempo real

# Posicionamiento inicial en la cancha (Escenario 5)
level2_wait_positions = [(-10.0, -18.0), (10.0, -18.0)]
level2_active_positions = [(-12.0, -14.0), (12.0, -14.0)]
level2_start_positions = [(-20.0, 0.0), (20.0, 0.0)]

# Desenlace del nivel 
level2_game_over = False
level2_winner = None               # Almacena 'p1', 'p2' o 'empate'
nuevo_balon_enemigo = {
    "x": 0.0,
    "y": 0.0,
    "z": -15.0,
    "vx": 0.0,
    "vy": 0.0,
    "vz": 0.3,
    "size": 1.2,
    "color": (1.0, 0.5, 0.0),
    "owner": "sistema"
}
level_balones_jugador.append(nuevo_balon_enemigo)