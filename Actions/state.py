# state.py
from Actions.colisiones import CollisionObject #importar la clase colisiones 
# estado inicial
expression = "neutral" 
show_instructions = True

#posicion fija
gato_x = 0.0
gato_z = 0.0

# tiempo y animaciones q,w,e,r
animation_angle = 0.0
tail_angle = 0.0
blink_timer = 0.0
leg_swing = 0.0
reaction_type = None
reaction_timer = 0
reaction_duration = 30
walking = False
moving_tail = False
blinking = False
waving = False

# camara
zoom = 10.5
mouse_down = False

scene_bounds = {
    "x": (-20.0, 20.0),
    "y": (-20.0, 20.0),
    "z": (0.0, 20.0)
}
# para reacciones
show_instructions = True
moving_tail = False   
blinking = False     
#escenarios
scenario = 1  # Empezamos en el Parque
#sonidos
sonido_activo = True
#ver si hay choque
hay_choque = False  

# creacion de los 3 objetos
objetos_escenas= [
    CollisionObject(5.0, 5.0, size=1.5, color=(0.6, 0.3, 0.1), label="Caja"),
    CollisionObject(-5.0, -8.0, size=1.0, color=(0.4, 0.4, 0.4), label="Piedra"),
    CollisionObject(0.0, -12.0, size=1.2, color=(0.1, 0.4, 0.1), label="Arbusto")
]

# animaciones nuevas 
arm_wave_angle = 0.0
ears_twitch_angle = 0.0
front_paws_up_angle = 0.0
arm_waving = False
ears_twitching = False
front_paws_up_active = False