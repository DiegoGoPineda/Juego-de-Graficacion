from OpenGL.GL import *

def draw_cube(x1, y1, z1, x2, y2, z2):
    glBegin(GL_QUADS)
    # Frontal
    glNormal3f(0, 0, 1)  # apunta hacia +z
    glVertex3f(x1, y1, z2); glVertex3f(x2, y1, z2); glVertex3f(x2, y2, z2); glVertex3f(x1, y2, z2)
    # Trasera
    glNormal3f(0, 0, -1)  # apunta hacia -z
    glVertex3f(x1, y1, z1); glVertex3f(x1, y2, z1); glVertex3f(x2, y2, z1); glVertex3f(x2, y1, z1)
    # Superior
    glNormal3f(0, 1, 0)  # apunta hacia +y
    glVertex3f(x1, y2, z1); glVertex3f(x1, y2, z2); glVertex3f(x2, y2, z2); glVertex3f(x2, y2, z1)
    # Inferior
    glNormal3f(0, -1, 0)  # apunta hacia -y
    glVertex3f(x1, y1, z1); glVertex3f(x2, y1, z1); glVertex3f(x2, y1, z2); glVertex3f(x1, y1, z2)
    # Derecha
    glNormal3f(1, 0, 0)  # apunta hacia +x
    glVertex3f(x2, y1, z1); glVertex3f(x2, y2, z1); glVertex3f(x2, y2, z2); glVertex3f(x2, y1, z2)
    # Izquierda
    glNormal3f(-1, 0, 0)  # apunta hacia -x
    glVertex3f(x1, y1, z1); glVertex3f(x1, y1, z2); glVertex3f(x1, y2, z2); glVertex3f(x1, y2, z1)
    glEnd()



    