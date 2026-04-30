# Actions/state.py
from Actions.colisiones import CollisionObject

class PlayerState:
    def __init__(self, x_inicial=0.0, nombre="Personaje", tipo="gato"):
        self.nombre = nombre
        self.tipo = tipo  
        self.x, self.y, self.z = x_inicial, 0.0, 0.0

        # --- Variables de Animación Comunes ---
        self.expression = "neutral"
        self.reaction_type = None
        self.reaction_timer = 0
        self.reaction_duration = 30
        self.walking = False
        self.animation_angle = 0.0
        self.leg_swing = 0.0
        
        # --- Variables compartidas (Gatos y Fox) ---
        self.moving_tail = False
        self.tail_angle = 0.0
        self.blinking = True
        self.blink_timer = 0.0
        
        # --- Variables específicas de Gatos (se quedan por compatibilidad) ---
        self.arm_waving = False
        self.arm_wave_angle = 0.0
        self.ears_twitching = False
        self.ears_twitch_angle = 0.0
        self.front_paws_up_active = False
        self.front_paws_up_angle = 0.0
        
        # --- Sistema de Colisión ---
        self.hay_choque = False
        self.color_colision_actual = (1.0, 1.0, 1.0)

# --- INSTANCIAS ---
# Ahora puedes definir los 6 personajes aquí, pero solo activamos 2
p1 = PlayerState(x_inicial=-3.0, nombre="Timoteo", tipo="gato")
#p2 = PlayerState(x_inicial=3.0, nombre="Lola", tipo="gato")
p2 = PlayerState(x_inicial=3.0, nombre="mosca", tipo="mosca")
# p3 = PlayerState(x_inicial=0.0, nombre="Fox", tipo="fox") # Este sería el tercero

# --- MUNDO ---
scenario = 1
sonido_activo = True
show_instructions = True
scene_bounds = {"x": (-20.0, 20.0), "z": (-20.0, 20.0)}

objetos_escenas = [
    CollisionObject(5.0, 5.0, 1.5, (0.6, 0.3, 0.1), "Caja", "surprised", "jump", "surprised"),
    CollisionObject(-5.0, -8.0, 1.0, (0.4, 0.4, 0.4), "Piedra", "angry", "shake", "angry"),
    CollisionObject(0.0, -12.0, 1.2, (0.1, 0.4, 0.1), "Arbusto", "interest", "spin", "interest"),
    CollisionObject(10.0, -5.0, 2.0, (0.3, 0.3, 0.7), "Contenedor", "fear", "shake", "fear"),
    CollisionObject(-10.0, 10.0, 0.8, (0.8, 0.2, 0.2), "Poste", "happy", "jump", "happy"),
    # objetos del zorro
    CollisionObject(0.0, -10.0, 1.2, (0.2, 0.8, 1.0), "Trampolin", "surprised", "jump"),
    CollisionObject(-10.0, 0.0, 1.0, (0.9, 0.1, 0.5), "Fruta Magica", "happy", "grow"),
    CollisionObject(10.0, -5.0, 0.8, (0.5, 0.0, 0.8), "Cristal Velocidad", "shouting", "flip")
]
