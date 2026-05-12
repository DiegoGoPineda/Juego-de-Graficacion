# camera.py
#Movimiento de camara y mouse 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from Actions import state 

cam_pos = [0.0, 1.5, 8.0]
yaw = 0.0
pitch = 0.0

cam_speed = 0.2
mouse_down = False
last_mouse_x = 0
last_mouse_y = 0

def apply_camera_to_player(player):
    global cam_pos, yaw, pitch
    
    glLoadIdentity()
    
    #  Ajuste de altura y distancia 
    # cam_pos[2] es la distancia hacia atrás.
    # El -1.8 en Y eleva la cámara para que mire un poco desde arriba
    distancia_atras = -cam_pos[2] 
    altura_camara = -1.8 
    
    glTranslatef(0, altura_camara, distancia_atras)
    glRotatef(-pitch, 1.0, 0.0, 0.0)
    
    # rotacion:
    # Hacemos que la camara gire según hacia donde mira el personaje.
    # Restamos 180 para que se coloque detras.
    glRotatef(player.direction_angle - 180, 0, 1, 0)
    
    # translacion
    # Movemos el mundo a la posición inversa del jugador
    glTranslatef(-player.x, -player.y, -player.z)

def handle_special_keys(key, x, y):
    pass

def mouse(button, button_state, x, y):
    global mouse_down, last_mouse_x, last_mouse_y
    # para sostener el click
    if button == GLUT_LEFT_BUTTON:
        mouse_down = (button_state == GLUT_DOWN)
        last_mouse_x = x
        last_mouse_y = y

def motion(x, y):
    global yaw, pitch, last_mouse_x, last_mouse_y

    if not mouse_down:
        return

    dx = x - last_mouse_x
    dy = y - last_mouse_y

    yaw += dx * 0.2
    pitch += dy * 0.2
    pitch = max(-89, min(89, pitch))

    last_mouse_x = x
    last_mouse_y = y

    glutPostRedisplay()

def zoom_in():
    global cam_pos
    # Acercamos la cámara reduciendo Z, con un limite para no atrevesar
    if cam_pos[2] > 2.0: 
        cam_pos[2] -= 0.5
    glutPostRedisplay()

def zoom_out():
    global cam_pos
    # Alejamos la cámara aumentando Z
    if cam_pos[2] < 30.0:
        cam_pos[2] += 0.5
    glutPostRedisplay()

def reset_camera():
    # Vista Normal (Reset)
    global cam_pos, yaw, pitch
    cam_pos = [0.0, 1.5, 6.0]
    yaw = 0.0
    pitch = 0.0
    glutPostRedisplay()

def view_top():
    # Vista Desde arriba
    global cam_pos, yaw, pitch
    cam_pos[2] = 8.0
    yaw, pitch = 0.0, -90.0 # Mirando hacia abajo
    glutPostRedisplay()

def view_side():
    # Vista Lateral
    global cam_pos, yaw, pitch
    cam_pos[2] = 8.0
    yaw, pitch = 90.0, 0.0 # Giro de 90 grados
    glutPostRedisplay()

def view_front_close():
    # Vista Frontal Cercana
    global cam_pos, yaw, pitch
    cam_pos[2] = 4.0 # Zoom fuerte
    yaw, pitch = 0.0, 10.0 # hacia abajao para ver la cara
    glutPostRedisplay()

def view_rear():
    # Vista Trasera
    global cam_pos, yaw, pitch
    cam_pos[2] = 8.0
    yaw, pitch = 180.0, 0.0 # Verlo por detrás
    glutPostRedisplay()
    