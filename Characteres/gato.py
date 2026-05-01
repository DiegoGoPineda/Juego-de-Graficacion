from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from Actions import state
from Utils.dibujar_cubo import draw_cube
from Actions.luz import set_color
def get_collision_color(p):
    return getattr(p, 'color_colision_actual', (1.0, 0.0, 0.0))

def draw_body(p):
    glPushMatrix()
    if p.hay_choque:
        set_color(*get_collision_color(p))
    else:
        set_color(0.1, 0.1, 0.1)
    
    draw_cube(0, 0, 1, 3, 1, 2)
    if not p.hay_choque:
        set_color(1.0, 1.0, 1.0)
        draw_cube(1.5, -0.01, 1.1, 3.01, 1.01, 1.9)
    glPopMatrix()

def draw_head(p):
    glPushMatrix()

    # Color base
    if p.hay_choque:
        
        set_color(*get_collision_color(p))
    else:
        set_color(0.1, 0.1, 0.1)
    draw_cube(3, 0, 1.5, 4, 1, 2.5)
    if not p.hay_choque:
        set_color(1.0, 1.0, 1.0)
        draw_cube(3.8, 0.2, 1.7, 4.01, 0.8, 2.3)

    # boca en el centro
    z_center = 2.0

    m_color = (0.2, 0.15, 0.1)
    y_min, y_max = 0.4, 0.6
    width = 0.3
    x_ext = 4.35

    if p.expression == "happy":
        m_color = (0.8, 0.4, 0.4)
        y_min, y_max = 0.25, 0.65
        width = 0.6

    elif p.expression == "sad":
        m_color = (0.1, 0.1, 0.3)
        # Boca más centrada 
        y_min, y_max = 0.35, 0.55   
        width = 0.5                 

    elif p.expression == "angry":
        m_color = (0.6, 0.0, 0.0)
        # Boca mas larga en ancho y altura
        y_min, y_max = 0.35, 0.75   
        width = 1.0                 

    elif p.expression == "surprised":
        m_color = (0.0, 0.0, 0.0)
        y_min, y_max = 0.2, 0.8
        width = 0.2

    elif p.expression == "fear":
        m_color = (0.3, 0.3, 0.3)
        y_min, y_max = 0.45, 0.55
        width = 0.6

    elif p.expression == "interest":
        m_color = (1.0, 0.8, 0.0)
        y_min, y_max = 0.4, 0.6
        width = 0.5

    z_min = z_center - width / 2
    z_max = z_center + width / 2

    set_color(*m_color)
    draw_cube(4, y_min, z_min, x_ext, y_max, z_max)

    glPopMatrix()

# ojos
def draw_eyes(p):
    is_blinking = math.sin(p.blink_timer) > 0.8

    z_center = 2.1  # centro en z

    for dy in [0.1, 0.7]:
        glPushMatrix()

        #  COLOR
        if p.expression == "angry":
            set_color(1.0, 0.0, 0.0)
        elif p.expression == "happy":
            set_color(1.0, 0.5, 0.8)
        elif p.expression == "sad":
            set_color(0.2, 0.2, 1.0)
        elif p.expression == "surprised":
            set_color(1.0, 1.0, 1.0)
        elif p.expression == "fear":
            set_color(1.0, 1.0, 0.0)
        elif p.expression == "interest":
            set_color(0.0, 1.0, 1.0)
        else:
            set_color(0.0, 0.8, 0.4)
        height = 0.2
        width = 0.2
        # reacciones
        if is_blinking or p.expression == "sad":
            height = 0.08  # ojos cerrados
        elif p.expression == "surprised":
            height = 0.35
            width = 0.3
        elif p.expression == "angry":
            height = 0.15
            width = 0.35
        elif p.expression == "happy":
            height = 0.15
            width = 0.3
        elif p.expression == "interest":
            height = 0.18
            width = 0.25
        z_min = z_center - width / 2
        z_max = z_center + width / 2
        y_min = dy
        y_max = dy + height
        draw_cube(4.01, y_min, z_min, 4.05, y_max, z_max)

        glPopMatrix()

# orejas
def draw_ears(p):
    glPushMatrix()
    if p.hay_choque:
        set_color(*get_collision_color(p))
    else:
        set_color(0.1, 0.1, 0.1)
    #oreja izquierda
    glTranslate(3.25, 0.2, 2.5)
    glRotate(p.ears_twitch_angle, 1, 0, 0)
    glTranslate(-3.25, -0.2, -2.5)
    draw_cube(3.1, 0.1, 2.5, 3.4, 0.3, 2.75)
    glPopMatrix()

    # Oreja Derecha
    glPushMatrix()
    glTranslate(3.25, 0.8, 2.5)
    glRotate(-p.ears_twitch_angle, 1, 0, 0)
    glTranslate(-3.25, -0.8, -2.5)
    draw_cube(3.1, 0.7, 2.5, 3.4, 0.9, 2.75)
    glPopMatrix()


# patas
def draw_legs(p):
    # Patas traseras (quietas o caminado normal)
    set_color(1.0, 1.0, 1.0)
    # Trasera Izq
    glPushMatrix()
    glTranslate(0.25, 0.25, 0.5)
    glRotate(p.leg_swing if p.walking else 0, 0, 1, 0)
    glTranslate(-0.25, -0.25, -0.5)
    draw_cube(0, 0, 0, 0.5, 0.5, 1)
    glPopMatrix()
    # Trasera Der
    glPushMatrix()
    glTranslate(0.25, 0.75, 0.5)
    glRotate(-p.leg_swing if p.walking else 0, 0, 1, 0)
    glTranslate(-0.25, -0.75, -0.5)
    draw_cube(0, 0.5, 0, 0.5, 1, 1)
    glPopMatrix()
    # patas enfrente (Con animaciones nuevas)
    # enfrente izquierda (Solo sube)
    glPushMatrix()
    glTranslate(2.75, 0.25, 0.5)
    if p.front_paws_up_active:
        glRotate(p.front_paws_up_angle, 0, -1, 0)
    elif p.walking:
        glRotate(-p.leg_swing, 0, 1, 0)
    glTranslate(-2.75, -0.25, -0.5)
    draw_cube(2.5, 0, 0, 3, 0.5, 1)
    glPopMatrix()
    # enfrente derecha (Saluda y sube)
    glPushMatrix()
    glTranslate(2.75, 0.75, 0.5)
    if p.front_paws_up_active:
        glRotate(p.front_paws_up_angle, 0, -1, 0)
    elif p.arm_waving:
        glRotate(p.arm_wave_angle, 0, 1, 0)
    elif p.walking:
        glRotate(p.leg_swing, 0, 1, 0)
    glTranslate(-2.75, -0.75, -0.5)
    draw_cube(2.5, 0.5, 0, 3, 1, 1)
    glPopMatrix()
# cola
def draw_tail(p):
    glPushMatrix()
    angle = math.sin(p.tail_angle) * 15
    glTranslate(0, 0.5, 1.8)
    glRotate(angle, 0, 1, 0)
    glTranslate(0, -0.5, -1.8)
    if p.hay_choque:
        set_color(*get_collision_color(p))
    else:
        set_color(0.1, 0.1, 0.1)

    draw_cube(-1.5, 0.37, 1.75, 0, 0.62, 2)

    set_color(1.0, 1.0, 1.0)
    draw_cube(-2.5, 0.37, 1.75, -1.5, 0.62, 2)

    glPopMatrix()

# collar
def draw_collar(p):
    glPushMatrix()
    if p.hay_choque:
        set_color(1.0, 1.0, 0.0)
    else:
        set_color(0.8, 0.0, 0.0)
    draw_cube(2.9, -0.05, 1.45, 3.1, 1.05, 2.55)
    set_color(1.0, 0.84, 0.0)
    draw_cube(3.05, 0.4, 1.85, 3.15, 0.6, 2.15)
    glPopMatrix()

def draw_gato_full(p):
    glPushMatrix()
 
    if p.reaction_type == "jump":
        y_offset = math.sin(math.pi * p.reaction_timer / p.reaction_duration) * 1.5
        glTranslatef(0, y_offset, 0)
    elif p.reaction_type == "spin":
        angle = 360 * (p.reaction_timer / p.reaction_duration)
        glRotatef(angle, 0, 1, 0)
    elif p.reaction_type == "shake":
        x_offset = math.sin(p.reaction_timer * 2.0) * 0.1
        glTranslatef(x_offset, 0, 0)

    glRotatef(-90, 0, 1, 0)
    glRotatef(-90, 1, 0, 0)
    glTranslatef(-1.5, -0.5, 0.0)
    draw_body(p)
    draw_head(p)
    draw_ears(p)
    draw_eyes(p)
    draw_collar(p)
    draw_legs(p)
    draw_tail(p)
    glPopMatrix()

    