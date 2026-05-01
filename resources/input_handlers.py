from OpenGL.GLUT import *
from Actions import state, camera, gestor_audio
import pygame

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

def special_keys(key, x, y):
    paso = 0.5 
    # si estamos se pueden mover 
    if state.estado_actual == state.EN_JUEGO:
        if key == GLUT_KEY_UP: 
            state.p2.z -= paso; state.p2.walking = True
        elif key == GLUT_KEY_DOWN:
             state.p2.z += paso; state.p2.walking = True
        elif key == GLUT_KEY_LEFT: 
            state.p2.x -= paso; state.p2.walking = True
        elif key == GLUT_KEY_RIGHT: 
            state.p2.x += paso; state.p2.walking = True
    
    glutPostRedisplay()
"""
def keyboard(key, x, y):
    b = key 
    if b in [b'1', b'2', b'3', b'4', b'5', b'6', b'7']:
        mapping = {
            b'1': ("neutral", 1, None),    # Parque - Normal
            b'2': ("happy", 2, "jump"),    # Callejón - Salta de alegría
            b'3': ("sad", 3, "shake"),     # Teatro - Tiembla de pena
            b'4': ("angry", 4, "spin"),    # Nieve - Gira de coraje
            b'5': ("surprised", 5, "jump"),# Volcán - Salta del susto
            b'6': ("fear", 6, "shake"),    # Desierto - Tiembla de miedo
            b'7': ("interest", 7, "spin")  # Espacio - Gira de curiosidad
        }
        
        exp, scn, react = mapping[b]
        #expresiones
        state.expression = exp
        # escenearios
        state.scenario = scn
        state.reaction_type = react
        state.reaction_timer = 0  
        # Sonidos vinculados
        gestor_audio.play_action_sound(state.expression)
        gestor_audio.play_background_music(state.scenario)
    elif b == b'w': 
        state.reaction_type, state.reaction_timer = "jump", 0
    elif b == b'a': 
        state.reaction_type, state.reaction_timer = "spin", 0
    elif b == b's': 
        state.walking = not state.walking
    elif b == b'd':
        state.moving_tail = not state.moving_tail
    elif b == b'i': 
        state.blinking = not state.blinking
    elif b == b'k': 
        state.arm_waving = not state.arm_waving
    elif b == b'l': 
        state.ears_twitching = not state.ears_twitching
    elif b == b'j':
        state.front_paws_up_active = not state.front_paws_up_active

    elif b == b'0': 
        state.show_instructions = not state.show_instructions
    elif b == b'o':
        state.sonido_activo = not state.sonido_activo
        if not state.sonido_activo:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
    
    elif b == b'z': camera.zoom_in()
    elif b == b'x': camera.zoom_out()
    elif b == b'c': camera.reset_camera()
    elif b == b'v': camera.view_top()
    elif b == b'b': camera.view_side()
    elif b == b'n': camera.view_front_close()
    elif b == b'm': camera.view_rear()
    elif key == b'\x1b': 
        glutLeaveMainLoop()
    glutPostRedisplay()
"""
#Versión mejorada para Multijugador y más controles de animación
def keyboard(key, x, y):
    b = key 
    paso = 0.5
    # --- 1. LÓGICA DEL MENÚ PRINCIPAL (BOTONES) ---
    if state.estado_actual == state.MENU_PRINCIPAL:
        if b == b'w' or b == b'W':
            state.indice_boton = 0 # JUGAR
            gestor_audio.play_action_sound("interest")
        elif b == b's' or b == b'S':
            state.indice_boton = 1 # SALIR
            gestor_audio.play_action_sound("interest")
            glutLeaveMainLoop()
        elif b == b'\r': # ENTER
            if state.indice_boton == 0:
                state.estado_actual = state.MENU_SELECCION
                state.en_menu_seleccion = True
                gestor_audio.play_action_sound("happy")
            else:
                sys.exit()
        elif key == b'\x1b': sys.exit()
        glutPostRedisplay()
        return

    # --- 2. LÓGICA DE SELECCIÓN DE PERSONAJES ---
    if state.estado_actual == state.MENU_SELECCION:
        if b == b'a' or b == b'd': 
            state.indice_menu = (state.indice_menu + (1 if b == b'd' else -1)) % len(state.personajes_pool)
            gestor_audio.play_action_sound("interest")
        
        elif b == b'\r': # ENTER (Confirmar selección)
            if state.fase_seleccion == 1:
                state.p1.tipo = state.personajes_pool[state.indice_menu].tipo
                state.fase_seleccion = 2
                gestor_audio.play_action_sound("happy")
            elif state.fase_seleccion == 2:
                state.p2.tipo = state.personajes_pool[state.indice_menu].tipo
                state.estado_actual = state.EN_JUEGO
                state.en_menu_seleccion = False 
                gestor_audio.play_action_sound("happy")
        
        elif key == b'\x1b': state.estado_actual = state.MENU_PRINCIPAL
        glutPostRedisplay()
        return
    # 1. movimientos timoteo
    if b == b'w': 
        state.p1.z -= paso
        state.p1.walking = True
    elif b == b's': 
        state.p1.z += paso
        state.p1.walking = True
    elif b == b'a': 
        state.p1.x -= paso
        state.p1.walking = True
    elif b == b'd': 
        state.p1.x += paso
        state.p1.walking = True

    # 2. ANIMACIONES MANUALES TIMOTEO (p1)
    # Usamos teclas cercanas: Q, E, R, F, G
    elif b == b'q': # Cola
        state.p1.moving_tail = not state.p1.moving_tail
    elif b == b'e': # Parpadeo
        state.p1.blinking = not state.p1.blinking
    elif b == b'r': # Reacción de Salto
        state.p1.reaction_type, state.p1.reaction_timer = "jump", 0
    elif b == b'f': # Saludar (Arm waving)
        state.p1.arm_waving = not state.p1.arm_waving
    elif b == b'g': # Patas arriba
        state.p1.front_paws_up_active = not state.p1.front_paws_up_active
        

    # 3. CAMBIO DE ESCENARIO (Afecta a Timoteo y Lola simultáneamente)
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
        
        # Aplicamos a AMBOS gatos
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
    # 4. CONTROLES DE CÁMARA Y SISTEMA (Globales)
    elif b == b'0': state.show_instructions = not state.show_instructions
    elif b == b'z': camera.zoom_in()
    elif b == b'x': camera.zoom_out()
    elif b == b'c': camera.reset_camera()
    elif b == b'v': camera.view_top()
    elif b == b'b': camera.view_side()
    elif b == b'n': camera.view_front_close()
    elif b == b'm': camera.view_rear()
    elif key == b'\x1b': # ESC
        glutLeaveMainLoop()

    glutPostRedisplay()

def keyboard_up(key, x, y):
    b = key 
    # cuando se deja de presionar una tecla de movimiento, el gato deja de caminar
    if b in [b'w', b'a', b's', b'd']:
        state.p1.walking = False
    glutPostRedisplay()

def keyboard_special_up(key, x, y):
    # si no se presiona no camina
    if key in [GLUT_KEY_UP, GLUT_KEY_DOWN, GLUT_KEY_LEFT, GLUT_KEY_RIGHT]:
        state.p2.walking = False
    glutPostRedisplay()