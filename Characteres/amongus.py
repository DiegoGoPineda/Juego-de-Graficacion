from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Actions import state
import math
from Actions.luz import set_color

def get_collision_color(p):
    return getattr(p, 'color_colision_actual', (1.0, 0.0, 0.0))

def set_material():
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.4, 0.0, 0.0, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 0.0, 0.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

def draw_body(p):
    glPushMatrix()
    if p.hay_choque:
        set_color(*get_collision_color(p))
    else:
        set_color(0.8, 0.0, 0.0)  # Rojo para el traje
    glTranslatef(0,1,0)
    glRotatef(-90,1,0,0)
    gluCylinder(gluNewQuadric(),1.2,1.2,2,32,32)
    glPopMatrix()

    glPushMatrix()
    if p.hay_choque:
        set_color(*get_collision_color(p))
    else:
        set_color(0.8, 0.0, 0.0)
    glTranslatef(0,3,0)
    glutSolidSphere(1.2,32,32)
    glPopMatrix()

def draw_visor(p):
    glPushMatrix()

    if p.hay_choque:
        set_color(*get_collision_color(p))
    else:
        set_color(0.4, 0.6, 0.9)  # Azul para el visor

    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.4, 0.6, 0.9, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.6, 0.9, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 100.0)

    glTranslatef(0.8, 2.5, 0)

    if p.expression == "angry":
        glRotatef(20,0,0,1)
    elif p.expression == "fear":
        glScalef(1.2,1.2,1.2)
    elif p.expression == "surprised":
        glScalef(1.3,1.3,1.3)
    elif p.expression == "happy":
        glScalef(1.1,1.1,1.1)

    glScalef(0.6,0.8,1.3)
    glutSolidSphere(1,32,32)

    glPopMatrix()

def draw_backpack(p):
    glPushMatrix()
    if p.hay_choque:
        set_color(*get_collision_color(p))
    else:
        set_color(0.1, 0.1, 0.1)  # Gris para la mochila
    glTranslatef(-1.2,2,0)
    glScalef(0.8,1.5,1.2)
    glutSolidCube(1)
    glPopMatrix()

def draw_legs(p):
    glPushMatrix()
    if p.hay_choque:
        set_color(*get_collision_color(p))
    else:
        set_color(0.8, 0.0, 0.0)

    for dz in [-0.7, 0.7]:
        glPushMatrix()
        glTranslatef(0,0,dz)

        if p.walking:
            glRotatef(p.leg_swing,1,0,0)

        glRotatef(-90,1,0,0)
        gluCylinder(gluNewQuadric(),0.5,0.5,1,16,16)
        glPopMatrix()
    glPopMatrix()

def draw_amongus_full(p):
    glPushMatrix()

    # Rotación según dirección de movimiento
    glRotatef(p.direction_angle, 0, 1, 0)
    glRotatef(-90, 0, 1, 0)
    
    # Escala reducida para que sea más pequeño
    glScalef(0.65, 0.65, 0.65)

    # Animaciones básicas
    if hasattr(p, 'walking') and p.walking:
        glTranslatef(math.sin(p.animation_angle)*0.5, 0, 0)

    set_material()
    draw_body(p)
    draw_visor(p)
    draw_backpack(p)
    draw_legs(p)

    glPopMatrix()