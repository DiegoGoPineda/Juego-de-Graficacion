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
    if key == GLUT_KEY_UP: 
        state.gato_z -= paso; state.walking = True
    elif key == GLUT_KEY_DOWN:
         state.gato_z += paso; state.walking = True
    elif key == GLUT_KEY_LEFT: 
        state.gato_x -= paso; state.walking = True
    elif key == GLUT_KEY_RIGHT: 
        state.gato_x += paso; state.walking = True

    # Verificación de colisiones con los objetos del escenario
    state.hay_choque = any(obj.check_collision(state.gato_x, state.gato_z, 1.5) 
                        for obj in state.objetos_escenas)
    glutPostRedisplay()

def keyboard(key, x, y):
    b = key 
    
    # escenarios-
    if b in [b'1', b'2', b'3', b'4', b'5', b'6', b'7']:
        mapping = {
            b'1': ("neutral", 1), b'2': ("happy", 2), b'3': ("sad", 3),
            b'4': ("angry", 4), b'5': ("surprised", 5), b'6': ("fear", 6),
            b'7': ("interest", 7)
        }
        exp, scn = mapping[b]
        state.expression = exp
        state.scenario = scn
        
        if b == b'6': # Caso especial para el miedo
            state.reaction_type, state.reaction_timer = "shake", 0
        
        # sonidos
        gestor_audio.play_action_sound(state.expression)
        gestor_audio.play_background_music(state.scenario)

    # --- animaciones-
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
    
    # instruccion y quitar musica
    elif b == b'0': 
        state.show_instructions = not state.show_instructions
    elif b == b'o':
        state.sonido_activo = not state.sonido_activo
        if not state.sonido_activo:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
    
    # Controles de camara
    elif b == b'z': camera.zoom_in()
    elif b == b'x': camera.zoom_out()
    elif b == b'c': camera.reset_camera()
    elif b == b'v': camera.view_top()
    elif b == b'b': camera.view_side()
    elif b == b'n': camera.view_front_close()
    elif b == b'm': camera.view_rear()
    
    elif key == b'\x1b': # Tecla ESC para salir
        glutLeaveMainLoop()

    glutPostRedisplay()