from OpenGL.GLUT import *
from Actions import state, camera, gestor_audio
import pygame
import math
import sys

def mouse(button, state_btn, x, y):
    if state_btn == GLUT_DOWN:
        if button == 3: 
            camera.zoom_in()
        elif button == 4: 
            camera.zoom_out()
    if button == GLUT_LEFT_BUTTON:
        state.mouse_down = (state_btn == GLUT_DOWN)
        state.last_mouse_x, state.last_mouse_y = x, y
        camera.mouse(button, state_btn, x, y)
    glutPostRedisplay()

def motion(x, y):
    if not state.mouse_down: return
    dx, dy = x - state.last_mouse_x, y - state.last_mouse_y
    camera.motion(x, y)
    state.last_mouse_x, state.last_mouse_y = x, y
    glutPostRedisplay()

def _move_player_camera_relative(player, x_dir, z_dir, paso):
    forward, right = camera.get_forward_right_vectors()
    dx = forward[0] * z_dir + right[0] * x_dir
    dz = forward[2] * z_dir + right[2] * x_dir
    player.x += dx * paso
    player.z += dz * paso
    if dx != 0 or dz != 0:
        player.walking = True
        player.direction_angle = camera.direction_angle_from_vector(dx, dz)


def special_keys(key, x, y):
    # Rastrear teclas presionadas
    if state.estado_actual == state.EN_JUEGO:
        if state.level1_enabled and state.level1_phase == state.LEVEL1_TRIVIA and not state.level1_trivia_answered and state.level1_question_target == 'p2':
            if key == GLUT_KEY_UP:
                state.level1_selected_option = (state.level1_selected_option - 1) % 3
                glutPostRedisplay()
                return
            elif key == GLUT_KEY_DOWN:
                state.level1_selected_option = (state.level1_selected_option + 1) % 3
                glutPostRedisplay()
                return
        if key == GLUT_KEY_UP:
            state.keys_pressed['up'] = True
        elif key == GLUT_KEY_DOWN:
            state.keys_pressed['down'] = True
        elif key == GLUT_KEY_LEFT:
            state.keys_pressed['left'] = True
        elif key == GLUT_KEY_RIGHT:
            state.keys_pressed['right'] = True
    elif state.estado_actual == state.MENU_ESCENARIO:
        cols = 3
        max_len = 7 if state.modo_juego == 'libre' else 3
        if key == GLUT_KEY_LEFT:
            if state.indice_escenario % cols > 0:
                state.indice_escenario -= 1
        elif key == GLUT_KEY_RIGHT:
            if state.indice_escenario % cols < cols - 1 and state.indice_escenario < max_len - 1:
                state.indice_escenario += 1
        elif key == GLUT_KEY_UP:
            if state.indice_escenario >= cols:
                state.indice_escenario -= cols
        elif key == GLUT_KEY_DOWN:
            if state.indice_escenario < max_len - cols:
                state.indice_escenario += cols
    elif state.estado_actual == state.MENU_PAUSA:
        if key == GLUT_KEY_UP:
            state.indice_pausa = (state.indice_pausa - 1) % len(state.pause_menu_options)
        elif key == GLUT_KEY_DOWN:
            state.indice_pausa = (state.indice_pausa + 1) % len(state.pause_menu_options)
    
    glutPostRedisplay()

#Versión mejorada para Multijugador y más controles de animación
def keyboard(key, x, y):
    b = key 
    paso = 0.5
    # logica del menu
    if state.estado_actual == state.MENU_PRINCIPAL:
        if b == b'w' or b == b'W':
            state.indice_boton = (state.indice_boton - 1) % 3
            gestor_audio.play_action_sound("interest")
        elif b == b's' or b == b'S':
            state.indice_boton = (state.indice_boton + 1) % 3
            gestor_audio.play_action_sound("interest")
        elif b == b'\r':
            if state.indice_boton == 0:
                state.modo_juego = 'niveles'
                state.fase_seleccion = 1
                state.indice_menu = 0
                state.estado_actual = state.MENU_SELECCION
                state.en_menu_seleccion = True
                gestor_audio.play_action_sound("happy")
            elif state.indice_boton == 1:
                state.modo_juego = 'libre'
                state.fase_seleccion = 1
                state.indice_menu = 0
                state.estado_actual = state.MENU_SELECCION
                state.en_menu_seleccion = True
                gestor_audio.play_action_sound("happy")
            elif state.indice_boton == 2:
                glutLeaveMainLoop()
                return
        elif key == b'\x1b': 
            glutLeaveMainLoop()
            return
        glutPostRedisplay()
        return
    if state.estado_actual == state.MENU_ESCENARIO:
        if b == b'\r':
            selected = (state.niveles_pool if state.modo_juego == 'niveles' else state.escenarios_pool)[state.indice_escenario]
            state.scenario = selected['id']
            # Actualizar límites de escena
            if state.scenario in state.scenario_bounds:
                state.scene_bounds = state.scenario_bounds[state.scenario]
            state.estado_actual = state.EN_JUEGO
            if state.scenario == 4 and state.modo_juego == 'niveles':
                state.level1_enabled = True
                state.level1_phase = state.LEVEL1_WAITING
                state.p1.x, state.p1.z = state.level1_wait_positions[0]
                state.p2.x, state.p2.z = state.level1_wait_positions[1]
            else:
                state.level1_enabled = False
                state.level1_phase = state.LEVEL1_NONE
                state.p1.x, state.p1.z = -3.0, 0.0
                state.p2.x, state.p2.z = 3.0, 0.0
            gestor_audio.play_background_music(state.scenario)
        elif state.modo_juego == 'libre':
            if b == b'1': state.indice_escenario = 0
            elif b == b'2': state.indice_escenario = 1
            elif b == b'3': state.indice_escenario = 2
            elif b == b'4': state.indice_escenario = 3
            elif b == b'5': state.indice_escenario = 4
            elif b == b'6': state.indice_escenario = 5
            elif b == b'7': state.indice_escenario = 6
        elif key == b'\x1b':
            state.estado_actual = state.MENU_PRINCIPAL
            state.fase_seleccion = 1
            state.indice_menu = 0
            state.en_menu_seleccion = False
            state.indice_escenario = 0
        glutPostRedisplay()
        return
    if state.estado_actual == state.MENU_PAUSA:
        if b == b'\r':
            if state.indice_pausa == 0:
                state.estado_actual = state.EN_JUEGO
            elif state.indice_pausa == 1:
                state.estado_actual = state.MENU_PRINCIPAL
                state.fase_seleccion = 1
                state.indice_menu = 0
                state.en_menu_seleccion = False
                state.indice_escenario = 0
                gestor_audio.stop_voices()
                gestor_audio.play_background_music(1)
            elif state.indice_pausa == 2:
                state.estado_actual = state.MENU_SELECCION
                state.fase_seleccion = 1
                state.indice_menu = 0
                state.en_menu_seleccion = True
                state.indice_escenario = 0
            elif state.indice_pausa == 3:
                state.estado_actual = state.MENU_AYUDA
        elif key == b'\x1b':
            state.estado_actual = state.EN_JUEGO
        glutPostRedisplay()
        return
    if state.estado_actual == state.MENU_AYUDA:
        if b == b'\r' or key == b'\x1b':
            state.estado_actual = state.MENU_PAUSA
        glutPostRedisplay()
        return
    # selecicon
    if state.estado_actual == state.MENU_SELECCION:
        if b == b'a' or b == b'd': 
            # Cambiamos el índice del personaje
            state.indice_menu = (state.indice_menu + (1 if b == b'd' else -1)) % len(state.personajes_pool)
            # Obtenemos el tipo de personaje actual (ej. "gato", "lola", "amongus")
            personaje_actual = state.personajes_pool[state.indice_menu].tipo
            gestor_audio.stop_voices()
            gestor_audio.play_character_selection_sound(personaje_actual)
            return
        elif b == b'\r': # confirmacion
            # Silenciamos cualquier voz de personaje al entrar al juego
            gestor_audio.stop_voices()     
            if state.fase_seleccion == 1:
                state.p1.tipo = state.personajes_pool[state.indice_menu].tipo
                state.fase_seleccion = 2
                gestor_audio.play_action_sound("happy")
            elif state.fase_seleccion == 2:
                state.p2.tipo = state.personajes_pool[state.indice_menu].tipo
                if state.modo_juego == 'libre':
                    state.estado_actual = state.MENU_ESCENARIO
                    state.indice_escenario = 0
                else:  # modo 'niveles'
                    state.estado_actual = state.MENU_ESCENARIO
                    state.indice_escenario = 0
                state.en_menu_seleccion = False 
                gestor_audio.play_action_sound("happy")
        elif key == b'\x1b': 
            state.estado_actual = state.MENU_PRINCIPAL
            gestor_audio.stop_voices()    
        glutPostRedisplay()
        return
    # Manejo de fin de nivel 1
    if state.estado_actual == state.EN_JUEGO and state.level1_enabled and state.level1_phase == state.LEVEL1_FINISHED:
        if b == b'r' or b == b'R':
            # Repetir nivel - volver a la sala de espera
            state.level1_enabled = True
            state.level1_phase = state.LEVEL1_WAITING
            state.p1.lives = 5
            state.p2.lives = 5
            state.p1.x, state.p1.z = state.level1_wait_positions[0]
            state.p2.x, state.p2.z = state.level1_wait_positions[1]
            state.level1_game_over = False
            state.level1_winner = None
            state.level1_loser = None
            glutPostRedisplay()
            return
        elif b == b's' or b == b'S':
            # Seleccionar nivel - volver al menú de selección
            state.estado_actual = state.MENU_ESCENARIO
            state.level1_enabled = False
            state.level1_phase = state.LEVEL1_NONE
            state.indice_escenario = 0
            state.p1.lives = 5
            state.p2.lives = 5
            state.level1_game_over = False
            state.level1_winner = None
            state.level1_loser = None
            glutPostRedisplay()
            return
    # Manejo de trivia del nivel 1
    if state.estado_actual == state.EN_JUEGO and state.level1_enabled and state.level1_phase == state.LEVEL1_TRIVIA and not state.level1_trivia_answered:
        if state.level1_question_target == 'p1':
            # Jugador 1: W/S para seleccionar, A para confirmar
            if b == b'w' or b == b'W':
                state.level1_selected_option = (state.level1_selected_option - 1) % 3
                return
            elif b == b's' or b == b'S':
                state.level1_selected_option = (state.level1_selected_option + 1) % 3
                return
            elif b == b'a' or b == b'A':
                is_correct = state.level1_selected_option == state.level1_current_question["correct"]
                from Actions import update as update_module
                update_module.process_level1_trivia_answer(is_correct)
                return
        else:  # P2
            # Jugador 2: ENTER para confirmar
            if b == b'\r':  # ENTER
                is_correct = state.level1_selected_option == state.level1_current_question["correct"]
                from Actions import update as update_module
                update_module.process_level1_trivia_answer(is_correct)
                return
    # movimientos timoteo y lola (rastrear teclas presionadas para movimiento simultáneo)
    if b == b'w':
        state.keys_pressed[b'w'] = True
    elif b == b's':
        state.keys_pressed[b's'] = True
    elif b == b'a':
        state.keys_pressed[b'a'] = True
    elif b == b'd':
        state.keys_pressed[b'd'] = True
    elif b == b'f' or b == b'F':  # salto con F para p1
        if not state.p1.is_jumping:
            state.p1.is_jumping = True
            state.p1.jump_velocity = 0.9
    # animaicones
    elif b == b'q': # Cola
        state.p1.moving_tail = not state.p1.moving_tail
    elif b == b'e': # Parpadeo
        state.p1.blinking = not state.p1.blinking
    elif b == b'r': # Reacción de Salto
        state.p1.reaction_type, state.p1.reaction_timer = "jump", 0
    elif b == b'h': # Saludar (Arm waving)
        state.p1.arm_waving = not state.p1.arm_waving
    elif b == b'g': # Patas arriba
        state.p1.front_paws_up_active = not state.p1.front_paws_up_active
    elif b == b' ':  # Salto jugador 2 con ESPACIO
        if not state.p2.is_jumping:
            state.p2.is_jumping = True
            state.p2.jump_velocity = 0.9
    # escenarios y expresiones (para ambos personajes)
    elif b in [b'1', b'2', b'3', b'4', b'5', b'6', b'7']:
        mapping = {
            b'1': ("neutral", 1, None),
            b'2': ("happy", 2, "jump"),
            b'3': ("sad", 3, "shake"),
            b'4': ("angry", 4, "spin"),
            b'5': ("surprised", 5, "jump"),
            b'6': ("fear", 6, "shake"),
            b'7': ("interest", 7, "spin")
        }
        exp, scn, react = mapping[b]
        state.scenario = scn  
        # Actualizar límites de escena
        if scn in state.scenario_bounds:
            state.scene_bounds = state.scenario_bounds[scn]
        # Aplicacion para los 2
        for p in [state.p1, state.p2]:
            p.expression = exp
            p.reaction_type = react
            p.reaction_timer = 0      
        gestor_audio.play_action_sound(exp)
        gestor_audio.play_background_music(state.scenario)
    elif b == b'o': # activar/desactivar audio
        state.sonido_activo = not state.sonido_activo
        if not state.sonido_activo:
            pygame.mixer_music.pause() #sonido desactivado
        else:
            pygame.mixer_music.unpause() #sonido de vuelta 
    elif b == b'z': camera.zoom_in()
    elif b == b'x': camera.zoom_out()
    elif b == b'c': camera.reset_camera()
    elif b == b'v': camera.view_top()
    elif b == b'b': camera.view_side()
    elif b == b'n': camera.view_front_close()
    elif b == b'm': camera.view_rear()
    elif key == b'\x1b':
        if state.estado_actual == state.EN_JUEGO:
            state.estado_actual = state.MENU_PAUSA
            state.indice_pausa = 0
        elif state.estado_actual == state.MENU_PAUSA:
            state.estado_actual = state.EN_JUEGO
        elif state.estado_actual == state.MENU_AYUDA:
            state.estado_actual = state.MENU_PAUSA
        else:
            glutLeaveMainLoop()
    glutPostRedisplay()

def keyboard_up(key, x, y):
    b = key 
    # Limpiar el estado de las teclas presionadas
    if b == b'w':
        state.keys_pressed[b'w'] = False
    elif b == b'a':
        state.keys_pressed[b'a'] = False
    elif b == b's':
        state.keys_pressed[b's'] = False
    elif b == b'd':
        state.keys_pressed[b'd'] = False
    glutPostRedisplay()

def keyboard_special_up(key, x, y):
    # Limpiar el estado de las teclas especiales presionadas
    if key == GLUT_KEY_UP:
        state.keys_pressed['up'] = False
    elif key == GLUT_KEY_DOWN:
        state.keys_pressed['down'] = False
    elif key == GLUT_KEY_LEFT:
        state.keys_pressed['left'] = False
    elif key == GLUT_KEY_RIGHT:
        state.keys_pressed['right'] = False
    glutPostRedisplay()