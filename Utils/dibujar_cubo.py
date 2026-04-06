from OpenGL.GL import *

def draw_cube(x1, y1, z1, x2, y2, z2):
    glBegin(GL_QUADS)
    # Frontal
    glVertex3f(x1, y1, z2); glVertex3f(x2, y1, z2); glVertex3f(x2, y2, z2); glVertex3f(x1, y2, z2)
    # Trasera
    glVertex3f(x1, y1, z1); glVertex3f(x1, y2, z1); glVertex3f(x2, y2, z1); glVertex3f(x2, y1, z1)
    # Superior
    glVertex3f(x1, y2, z1); glVertex3f(x1, y2, z2); glVertex3f(x2, y2, z2); glVertex3f(x2, y2, z1)
    # Inferior
    glVertex3f(x1, y1, z1); glVertex3f(x2, y1, z1); glVertex3f(x2, y1, z2); glVertex3f(x1, y1, z2)
    # Derecha
    glVertex3f(x2, y1, z1); glVertex3f(x2, y2, z1); glVertex3f(x2, y2, z2); glVertex3f(x2, y1, z2)
    # Izquierda
    glVertex3f(x1, y1, z1); glVertex3f(x1, y1, z2); glVertex3f(x1, y2, z2); glVertex3f(x1, y2, z1)
    glEnd()