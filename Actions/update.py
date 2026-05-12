# actions/update.py
from OpenGL.GLUT import *
from Actions import state
from Actions import gestor_audio
import math

def enforce_scene_bounds(player):
    x_min, x_max = state.scene_bounds["x"]
    z_min, z_max = state.scene_bounds["z"]
    player.x = max(x_min, min(x_max, player.x))
    player.z = max(z_min, min(z_max, player.z))

def update_jugador_logica(player):
    enforce_scene_bounds(player)
    actualmente_colisionando = False
    objeto_tocado = None
    # solo cuandos se juega
    if state.estado_actual == state.EN_JUEGO:
        for obj in state.objetos_escenas:
            if obj.check_collision(player.x, player.z, 1.5):
                actualmente_colisionando = True
                objeto_tocado = obj
                break 
        # cuando hay choque
        if actualmente_colisionando and not player.hay_choque:
            player.expression = objeto_tocado.expresion
            player.reaction_type = objeto_tocado.animacion
            player.reaction_timer = 0
            player.color_colision_actual = objeto_tocado.color
            gestor_audio.play_action_sound(objeto_tocado.expresion)
    else:
        # no se juega
        actualmente_colisionando = False
    player.hay_choque = actualmente_colisionando
    # para el zorro y su movimiento 
    player.animation_angle += 0.15
    # Actualizamos timers y ángulos de este jugador
    if player.blinking:
        player.blink_timer += 0.1
    if player.moving_tail:
        player.tail_angle += 0.1
    if player.walking:
        #movimento de las patas
        player.animation_angle += 0.15
        player.leg_swing = math.sin(player.animation_angle) * 30
    else:
        player.leg_swing = 0
    if player.reaction_type:
        player.reaction_timer += 1
        if player.reaction_timer >= player.reaction_duration:
            player.reaction_type = None
            player.reaction_timer = 0
    # Animaciones extra (saludar, orejas, etc.)
    t_blink = player.blink_timer
    if player.arm_waving:
        player.arm_wave_angle = math.sin(t_blink * 8) * 35 
    else:
        player.arm_wave_angle = 0
    if player.ears_twitching:   
        player.ears_twitch_angle = math.sin(t_blink * 15) * 20
    else:
        player.ears_twitch_angle = 0
    player.front_paws_up_angle = 70 if player.front_paws_up_active else 0

def update(value):
    # Actualizar a los personajes
    update_jugador_logica(state.p1)
    
    # Actualizamos a Lola
    update_jugador_logica(state.p2)

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)