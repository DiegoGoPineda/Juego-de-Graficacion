from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Actions import state
import math
from Actions.luz import set_color

def get_collision_color(p):
    return getattr(p, 'color_colision_actual', (1.0, 0.0, 0.0))

def set_material():
    """Configura los materiales para el renderizado normal con luz."""
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.4, 0.0, 0.0, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 0.0, 0.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

def draw_body(p, shadow):
    glPushMatrix()
    if not shadow:
        if p.hay_choque:
            set_color(*get_collision_color(p))
        else:
            set_color(0.8, 0.0, 0.0)  # Rojo base
    
    # Cuerpo cilíndrico
    glTranslatef(0, 1, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 1.2, 1.2, 2, 32, 32)
    glPopMatrix()

    # Cabeza (Esfera superior)
    glPushMatrix()
    if not shadow:
        if p.hay_choque:
            set_color(*get_collision_color(p))
        else:
            set_color(0.8, 0.0, 0.0)
    glTranslatef(0, 3, 0)
    glutSolidSphere(1.2, 32, 32)
    glPopMatrix()

def draw_visor(p, shadow):
    glPushMatrix()
    if not shadow:
        if p.hay_choque:
            set_color(*get_collision_color(p))
        else:
            set_color(0.4, 0.6, 0.9)  # Azul visor
        
        # Brillo específico para el cristal del visor
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.4, 0.6, 0.9, 1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.6, 0.9, 1.0, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 100.0)

    glTranslatef(0.8, 2.5, 0)

    # Expresiones
    if p.expression == "angry":
        glRotatef(20, 0, 0, 1)
    elif p.expression == "fear":
        glScalef(1.2, 1.2, 1.2)
    elif p.expression == "surprised":
        glScalef(1.3, 1.3, 1.3)
    elif p.expression == "happy":
        glScalef(1.1, 1.1, 1.1)

    glScalef(0.6, 0.8, 1.3)
    glutSolidSphere(1, 32, 32)
    glPopMatrix()

def draw_backpack(p, shadow):
    glPushMatrix()
    if not shadow:
        if p.hay_choque:
            set_color(*get_collision_color(p))
        else:
            set_color(0.1, 0.1, 0.1)  # Gris oscuro
    
    glTranslatef(-1.2, 2, 0)
    glScalef(0.8, 1.5, 1.2)
    glutSolidCube(1)
    glPopMatrix()

def draw_legs(p, shadow):
    glPushMatrix()
    if not shadow:
        if p.hay_choque:
            set_color(*get_collision_color(p))
        else:
            set_color(0.8, 0.0, 0.0)

    for dz in [-0.7, 0.7]:
        glPushMatrix()
        glTranslatef(0, 0, dz)

        if p.walking:
            glRotatef(p.leg_swing, 1, 0, 0)

        glRotatef(-90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 0.5, 0.5, 1, 16, 16)
        glPopMatrix()
    glPopMatrix()

def draw_amongus_full(p):
    # Detectamos si estamos dibujando la sombra
    is_shadow = getattr(p, 'is_shadow_pass', False)

    glPushMatrix()

    # Transformaciones globales del personaje
    glRotatef(p.direction_angle, 0, 1, 0)
    glRotatef(-90, 0, 1, 0)
    glScalef(0.65, 0.65, 0.65)

    # Animación de rebote al caminar
    if hasattr(p, 'walking') and p.walking:
        glTranslatef(math.sin(p.animation_angle) * 0.2, 0, 0)

    if is_shadow:
        # Lógica de Sombra: Desactivamos luces y forzamos color oscuro
        glDisable(GL_LIGHTING)
        glColor4f(0.1, 0.1, 0.1, 0.5) # Color gris oscuro traslúcido
        
        draw_body(p, True)
        draw_visor(p, True)
        draw_backpack(p, True)
        draw_legs(p, True)
        
        glEnable(GL_LIGHTING)
    else:
        # Lógica Normal: Con materiales y colores
        set_material()
        draw_body(p, False)
        draw_visor(p, False)
        draw_backpack(p, False)
        draw_legs(p, False)

    glPopMatrix()