# actions/update.py
from OpenGL.GLUT import *
from Actions import state
import math


def enforce_scene_bounds():
    x_min, x_max = state.scene_bounds["x"]
    z_min, z_max = state.scene_bounds["z"]

    # Limitar gato dentro de los límites de la escena
    state.gato_x = max(x_min, min(x_max, state.gato_x))
    state.gato_z = max(z_min, min(z_max, state.gato_z))


def update(value):
    state.hay_choque = False
    for obj in state.objetos_escenas:
        if obj.check_collision(state.gato_x, state.gato_z):
            state.hay_choque = True
            break

    if state.blinking:
        state.blink_timer += 0.1

    # Movimiento de cola constante si state.moving_tail es True
    if state.moving_tail:
        state.tail_angle += 0.1
    
    # Movimiento de patas constante si state.walking es True
    if state.walking:
        state.animation_angle += 0.15
        state.leg_swing = math.sin(state.animation_angle) * 30
    else:
        state.leg_swing = 0 # Vuelve a posición neutral al apagar
    
    if state.reaction_type:
        state.reaction_timer += 1
        # Cuando el timer llega al límite, se detiene solo (Type = None)
        if state.reaction_timer >= state.reaction_duration:
            state.reaction_type = None
            state.reaction_timer = 0

    t = state.blink_timer
    #Saludar : Movimiento lateral rápido
    if state.arm_waving:
        # Un balanceo lateral (sinusoidal)
        state.arm_wave_angle = math.sin(t * 8) * 35 
    else:
        state.arm_wave_angle = 0

    #  Movimiento rapido y corto de las orejas
    if state.ears_twitching:
        # Balanceo muy rápido 
        state.ears_twitch_angle = math.sin(t * 15) * 20
    else:
        state.ears_twitch_angle = 0
    # Patas hacia enfrente
    if state.front_paws_up_active:
        # Movimiento de subida controlado (escala de 0 a 1)
        state.front_paws_up_angle = 70 # angulo fijo hacia arriba
    else:
        state.front_paws_up_angle = 0

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

