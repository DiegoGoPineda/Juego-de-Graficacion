# camera.py
#Movimiento de camara y mouse 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from Actions import state 

cam_pos = [0.0, 4.0, 14.0]
yaw = 0.0
pitch = -10.0

cam_speed = 0.2
mouse_down = False
last_mouse_x = 0
last_mouse_y = 0

def _get_yaw_radians():
    return math.radians(yaw)


def get_forward_right_vectors():
    rad = _get_yaw_radians()
    # Forward hacia donde mira la cámara en el plano XZ
    forward = (-math.sin(rad), 0.0, -math.cos(rad))
    right = (math.cos(rad), 0.0, -math.sin(rad))
    return forward, right


def direction_angle_from_vector(dx, dz):
    angle = math.degrees(math.atan2(dx, dz))
    return angle % 360


def apply_camera_to_player(player):
    global cam_pos, yaw, pitch
    glLoadIdentity()

    eye_height = 1.8
    distance = cam_pos[2]
    rad_yaw = _get_yaw_radians()
    rad_pitch = math.radians(pitch)

    cam_x = player.x + distance * math.sin(rad_yaw) * math.cos(rad_pitch)
    cam_y = player.y + cam_pos[1] + distance * math.sin(rad_pitch)
    cam_z = player.z + distance * math.cos(rad_yaw) * math.cos(rad_pitch)
    
    # Limitar la cámara dentro de los límites del escenario
    x_min, x_max = state.scene_bounds["x"]
    z_min, z_max = state.scene_bounds["z"]
    
    # Agregar margen de seguridad para que no penetre las paredes
    margin = 2.0
    cam_x = max(x_min + margin, min(x_max - margin, cam_x))
    cam_z = max(z_min + margin, min(z_max - margin, cam_z))
    cam_y = max(1.0, cam_y)  # No permitir que vaya debajo del suelo

    gluLookAt(cam_x, cam_y, cam_z,
              player.x, player.y + eye_height, player.z,
              0.0, 1.0, 0.0)

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
    cam_pos = [0.0, 4.0, 14.0]
    yaw = 0.0
    pitch = -10.0
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
    