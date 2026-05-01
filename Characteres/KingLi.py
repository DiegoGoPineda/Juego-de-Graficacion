from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from Actions import state
from Actions.luz import set_color

# Creamos un quadric local para esta clase
_q = gluNewQuadric()
gluQuadricNormals(_q, GLU_SMOOTH)

def apply_kingli_style(color, shininess=30.0):
    set_color(*color)
    
    if not state.is_shadow_pass:
        # Si el color es muy oscuro, eliminamos el brillo para evitar el efecto 'lavado'
        if sum(color[:3]) < 0.1:
            glMaterialfv(GL_FRONT, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
        else:
            glMaterialfv(GL_FRONT, GL_SPECULAR, [0.4, 0.4, 0.4, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, shininess)

def draw_aesthetic_cube(width, height, depth):
    glPushMatrix()
    glScalef(width, height, depth)
    glBegin(GL_QUADS)
    glNormal3f(0,0,1);  glVertex3f(-0.5,-0.5, 0.5); glVertex3f( 0.5,-0.5, 0.5); glVertex3f( 0.5, 0.5, 0.5); glVertex3f(-0.5, 0.5, 0.5)
    glNormal3f(0,0,-1); glVertex3f(-0.5,-0.5,-0.5); glVertex3f(-0.5, 0.5,-0.5); glVertex3f( 0.5, 0.5,-0.5); glVertex3f( 0.5,-0.5,-0.5)
    glNormal3f(0,1,0);  glVertex3f(-0.5, 0.5,-0.5); glVertex3f(-0.5, 0.5, 0.5); glVertex3f( 0.5, 0.5, 0.5); glVertex3f( 0.5, 0.5,-0.5)
    glNormal3f(0,-1,0); glVertex3f(-0.5,-0.5,-0.5); glVertex3f( 0.5,-0.5,-0.5); glVertex3f( 0.5,-0.5, 0.5); glVertex3f(-0.5,-0.5, 0.5)
    glNormal3f(1,0,0);  glVertex3f( 0.5,-0.5,-0.5); glVertex3f( 0.5, 0.5,-0.5); glVertex3f( 0.5, 0.5, 0.5); glVertex3f( 0.5,-0.5, 0.5)
    glNormal3f(-1,0,0); glVertex3f(-0.5,-0.5,-0.5); glVertex3f(-0.5,-0.5, 0.5); glVertex3f(-0.5, 0.5, 0.5); glVertex3f(-0.5, 0.5,-0.5)
    glEnd()
    glPopMatrix()

def draw_curly_hair():
    posiciones = [
        (0.0, 0.45, 0.0), (0.28, 0.25, 0.0), (-0.28, 0.25, 0.0), 
        (0.25, 0.35, -0.1), (-0.25, 0.35, -0.1), (0.12, 0.15, -0.22), 
        (-0.12, 0.15, -0.22), (0.0, 0.20, -0.25), (0.20, 0.10, -0.15), 
        (-0.20, 0.10, -0.15), (0.0, 0.52, 0.05), (0.15, 0.50, 0.10), 
        (-0.15, 0.50, 0.10), (0.0, 0.48, -0.1)
    ]
    for x, y, z in posiciones:
        glPushMatrix()
        glTranslatef(x, y, z)
        seed = (x * 13 + y * 7 + z * 5)
        var = 0.90 + (0.15 * ((math.sin(seed) + 1)/2))
        # Pelo casi negro, muy poco brillo
        apply_kingli_style([0.08 * var, 0.05 * var, 0.02 * var], 5.0)
        gluSphere(_q, 0.18, 15, 15)
        glPopMatrix()

def draw_aesthetic_glasses():
    # Marco negro profundo
    apply_kingli_style([0.01, 0.01, 0.01], 10.0)
    glPushMatrix(); glTranslatef(0.0, 0.05, 0.36); glScalef(0.1, 0.03, 0.02); draw_aesthetic_cube(1, 1, 1); glPopMatrix()
    for offset in [-0.15, 0.15]:
        glPushMatrix(); glTranslatef(offset, 0.12, 0.36); glScalef(0.2, 0.03, 0.02); draw_aesthetic_cube(1, 1, 1); glPopMatrix()
    
    # Cristales con transparencia 
    if not state.is_shadow_pass:
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        set_color(0.1, 0.1, 0.1, 0.5) # Color ahumado transparente
        for offset in [-0.15, 0.15]:
            glPushMatrix(); glTranslatef(offset, 0.05, 0.355); glScalef(0.19, 0.13, 0.01); draw_aesthetic_cube(1, 1, 1); glPopMatrix()
        glDisable(GL_BLEND)

def draw_face(p):
    exp = "sorprendido" if p.hay_choque else "feliz"
    ojos_y = 0.12 if exp == "feliz" else 0.1
    ojos_scale = 0.08 if exp == "sorprendido" else 0.06
    
    # negro total
    apply_kingli_style([0.0, 0.0, 0.0], 0.0)
    
    for side in [-0.15, 0.15]:
        glPushMatrix(); glTranslatef(side, ojos_y, 0.35); glScalef(ojos_scale, ojos_scale, 0.01); draw_aesthetic_cube(1,1,1); glPopMatrix()
    
    boca_h = 0.03 if exp == "sorprendido" else 0.08
    glPushMatrix(); glTranslatef(0.0, -0.1, 0.35); glScalef(0.2, boca_h, 0.01); draw_aesthetic_cube(1,1,1); glPopMatrix()

def draw_kingli_full(p):
    color_skin = [0.95, 0.8, 0.7]
    color_torso = [0.0, 0.15, 0.4]
    color_manga = [0.1, 0.25, 0.5]
    color_piernas = [0.35, 0.35, 0.35]
    
    if p.hay_choque:
        color_torso = p.color_colision_actual
        color_manga = [min(1.0, c * 1.2) for c in p.color_colision_actual]
    
    walk_angle = p.leg_swing 
    
    glPushMatrix()
    glTranslatef(0, 0.4, 0)
    
    # Reacciones
    if p.reaction_type == "jump":
        y_off = math.sin(math.pi * p.reaction_timer / p.reaction_duration) * 1.5
        glTranslatef(0, y_off, 0)
    elif p.reaction_type == "spin":
        glRotatef(360 * (p.reaction_timer / p.reaction_duration), 0, 1, 0)

    # Cuerpo
    apply_kingli_style(color_torso, 20.0)
    glPushMatrix(); glTranslatef(0, 0.85, 0); draw_aesthetic_cube(1.2, 1.4, 0.7); glPopMatrix()

    # Extremidades
    for side in [-1, 1]:
        # Piernas
        glPushMatrix()
        glTranslatef(side * 0.3, 0.1, 0.0)
        glRotatef(side * -walk_angle, 1, 0, 0)
        apply_kingli_style(color_piernas, 5.0)
        draw_aesthetic_cube(0.38, 1.0, 0.38)
        glPopMatrix()
        
        # Brazos
        glPushMatrix()
        glTranslatef(side * 0.75, 1.45, 0.0)
        glRotatef(180, 1, 0, 0)
        glRotatef(side * walk_angle, 1, 0, 0)
        
        apply_kingli_style(color_manga, 15.0)
        glTranslatef(0, 0.45, 0)
        draw_aesthetic_cube(0.32, 0.9, 0.32)
        
        # Mano
        glTranslatef(0, 0.5, 0)
        apply_kingli_style(color_skin, 10.0)
        gluSphere(_q, 0.18, 20, 20)
        glPopMatrix()

    # Cabeza
    glPushMatrix()
    glTranslatef(0, 1.9, 0)
    apply_kingli_style(color_skin, 10.0)
    gluSphere(_q, 0.35, 30, 30)
    
    draw_face(p)
    draw_aesthetic_glasses()
    draw_curly_hair()
    glPopMatrix()
    
    glPopMatrix()