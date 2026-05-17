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

def keyboard(key, x, y):
    b = key 
    paso = 0.5
    
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

            if state.scenario == 5 and state.modo_juego == 'niveles':
                state.level2_game_over = False
                state.level2_winner = None
                state.level2_phase = state.LEVEL2_WAITING
                state.level2_transition_alpha = 0.0
                state.level2_countdown = 3
                state.level2_countdown_timer = 0
                state.level2_message = "CARGANDO NIVEL 2..."
                state.level_balones_jugador = []
                state.level_balones_spawn_timer = 0
                state.p1.lives = 5
                state.p2.lives = 5
                state.p1.x, state.p1.z = state.level2_wait_positions[0]
                state.p2.x, state.p2.z = state.level2_wait_positions[1]
            else:
                state.level2_game_over = False

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

    if state.estado_actual == state.MENU_SELECCION:
        if b == b'a' or b == b'd': 
            state.indice_menu = (state.indice_menu + (1 if b == b'd' else -1)) % len(state.personajes_pool)
            personaje_actual = state.personajes_pool[state.indice_menu].tipo
            gestor_audio.stop_voices()
            gestor_audio.play_character_selection_sound(personaje_actual)
            return
        elif b == b'\r': 
            gestor_audio.stop_voices()     
            if state.fase_seleccion == 1:
                state.p1.tipo = state.personajes_pool[state.indice_menu].tipo
                state.fase_seleccion = 2
                gestor_audio.play_action_sound("happy")
            elif state.fase_seleccion == 2:
                state.p2.tipo = state.personajes_pool[state.indice_menu].tipo
                state.estado_actual = state.MENU_ESCENARIO
                state.indice_escenario = 0
                state.en_menu_seleccion = False 
                gestor_audio.play_action_sound("happy")
        elif key == b'\x1b': 
            state.estado_actual = state.MENU_PRINCIPAL
            gestor_audio.stop_voices()    
        glutPostRedisplay()
        return

    if state.estado_actual == state.EN_JUEGO and state.level1_enabled and state.level1_phase == state.LEVEL1_FINISHED:
        if b == b'r' or b == b'R':
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
            state.estado_actual = state.MENU_ESCENARIO
            state.level1_enabled = False
            state.level1_phase = state.LEVEL1_NONE
            state.indice_escenario = 0
            state.p1.lives = 5
            state.p2.lives = 5
            state.p1.game_over = False
            state.level1_winner = None
            state.level1_loser = None
            glutPostRedisplay()
            return

    if state.estado_actual == state.EN_JUEGO and state.scenario == 5 and getattr(state, 'level2_game_over', False):
        if b == b'r' or b == b'R':
            state.p1.lives = 5
            state.p2.lives = 5
            state.level2_game_over = False
            state.level2_winner = None
            state.level2_phase = state.LEVEL2_WAITING
            state.level2_transition_alpha = 0.0
            state.level2_countdown = 3
            state.level2_countdown_timer = 0
            state.level2_message = "CARGANDO NIVEL 2..."
            if hasattr(state, 'level_balones_jugador'):
                state.level_balones_jugador.clear()
            state.level_balones_spawn_timer = 0
            state.p1.x, state.p1.z = state.level2_wait_positions[0]
            state.p2.x, state.p2.z = state.level2_wait_positions[1]
            gestor_audio.play_action_sound("happy")
            glutPostRedisplay()
            return
        elif b == b's' or b == b'S':
            state.estado_actual = state.MENU_ESCENARIO
            state.indice_escenario = 0
            state.p1.lives = 5
            state.p2.lives = 5
            state.level2_game_over = False
            state.level2_winner = None
            state.level2_phase = getattr(state, 'LEVEL2_NONE', 0)
            if hasattr(state, 'level_balones_jugador'):
                state.level_balones_jugador.clear()
            glutPostRedisplay()
            return

    if state.estado_actual == state.EN_JUEGO and state.level1_enabled and state.level1_phase == state.LEVEL1_TRIVIA and not state.level1_trivia_answered:
        if state.level1_question_target == 'p1':
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
        else: 
            if b == b'\r':  
                is_correct = state.level1_selected_option == state.level1_current_question["correct"]
                from Actions import update as update_module
                update_module.process_level1_trivia_answer(is_correct)
                return

    if b == b'w': state.keys_pressed[b'w'] = True
    elif b == b's': state.keys_pressed[b's'] = True
    elif b == b'a': state.keys_pressed[b'a'] = True
    elif b == b'd': state.keys_pressed[b'd'] = True
        
    # ACCIÓN / DISPARO JUGADOR 1 (E / e) Basado en dirección del jugador
    elif b == b'e' or b == b'E':
        if state.estado_actual == state.EN_JUEGO and state.scenario == 5 and state.level2_phase == state.LEVEL2_WAITING:
            state.level2_phase = state.LEVEL2_TRANSITION
            state.level2_transition_alpha = 0.0
            state.level2_message = "CARGANDO NIVEL 2..."
            state.level2_countdown = 3
            state.level2_countdown_timer = 0
            return
        if getattr(state, 'level_balones_enabled', False) and state.estado_actual == state.EN_JUEGO and state.level2_phase == state.LEVEL2_ACTIVE:
            if state.level2_cooldown_p1 == 0:
                rad = math.radians(state.p1.direction_angle)
                dir_x = math.sin(rad)
                dir_z = math.cos(rad)
                speed = 0.45 * state.level2_ball_speed_multiplier
                
                nuevo_balon = {
                    'x': state.p1.x + (dir_x * 1.2),
                    'y': 0.0,
                    'z': state.p1.z + (dir_z * 1.2),
                    'vx': dir_x * speed, 
                    'vy': 0.0,
                    'vz': dir_z * speed,
                    'size': 1.2,
                    'color': (0.2, 0.6, 1.0), 
                    'owner': 'p1'
                }
                state.level_balones_jugador.append(nuevo_balon)
                state.level2_cooldown_p1 = 20 
                gestor_audio.play_action_sound("angry")
        else:
            state.p1.blinking = not state.p1.blinking
            
    elif b == b'f' or b == b'F': 
        if not state.p1.is_jumping:
            state.p1.is_jumping = True
            state.p1.jump_velocity = 0.9
            
    # DISPARO JUGADOR 2 (ENTER) Basado en dirección del jugador
    elif b == b'\r':
        if state.estado_actual == state.EN_JUEGO and state.scenario == 5 and state.level2_phase == state.LEVEL2_WAITING:
            state.level2_phase = state.LEVEL2_TRANSITION
            state.level2_transition_alpha = 0.0
            state.level2_message = "CARGANDO NIVEL 2..."
            state.level2_countdown = 3
            state.level2_countdown_timer = 0
            return
        if getattr(state, 'level_balones_enabled', False) and state.estado_actual == state.EN_JUEGO and state.level2_phase == state.LEVEL2_ACTIVE:
            if state.level2_cooldown_p2 == 0:
                rad = math.radians(state.p2.direction_angle)
                dir_x = math.sin(rad)
                dir_z = math.cos(rad)
                speed = 0.45 * state.level2_ball_speed_multiplier
                
                nuevo_balon = {
                    'x': state.p2.x + (dir_x * 1.2),
                    'y': 0.0,
                    'z': state.p2.z + (dir_z * 1.2),
                    'vx': dir_x * speed, 
                    'vy': 0.0,
                    'vz': dir_z * speed,
                    'size': 1.2,
                    'color': (0.2, 1.0, 0.4), 
                    'owner': 'p2'
                }
                state.level_balones_jugador.append(nuevo_balon)
                state.level2_cooldown_p2 = 20 
                gestor_audio.play_action_sound("angry")
            return 
           
    elif b == b' ': 
        if not state.p2.is_jumping:
            state.p2.is_jumping = True
            state.p2.jump_velocity = 0.9
            
    elif b == b'q': state.p1.moving_tail = not state.p1.moving_tail
    elif b == b'r': state.p1.reaction_type, state.p1.reaction_timer = "jump", 0
    elif b == b'h': state.p1.arm_waving = not state.p1.arm_waving
    elif b == b'g': state.p1.front_paws_up_active = not state.p1.front_paws_up_active
        
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
        if scn in state.scenario_bounds:
            state.scene_bounds = state.scenario_bounds[scn]
            
        for p in [state.p1, state.p2]:
            p.expression = exp
            p.reaction_type = react
            p.reaction_timer = 0      
        gestor_audio.play_action_sound(exp)
        gestor_audio.play_background_music(state.scenario)
        
    elif b == b'o': 
        state.sonido_activo = not state.sonido_activo
        if not state.sonido_activo:
            pygame.mixer_music.pause()
        else:
            pygame.mixer_music.unpause()
            
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
    if b == b'w': state.keys_pressed[b'w'] = False
    elif b == b'a': state.keys_pressed[b'a'] = False
    elif b == b's': state.keys_pressed[b's'] = False
    elif b == b'd': state.keys_pressed[b'd'] = False
    glutPostRedisplay()

def keyboard_special_up(key, x, y):
    if key == GLUT_KEY_UP: state.keys_pressed['up'] = False
    elif key == GLUT_KEY_DOWN: state.keys_pressed['down'] = False
    elif key == GLUT_KEY_LEFT: state.keys_pressed['left'] = False
    elif key == GLUT_KEY_RIGHT: state.keys_pressed['right'] = False
    glutPostRedisplay()