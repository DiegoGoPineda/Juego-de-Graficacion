from OpenGL.GL import *
from Characteres.gato import draw_cube  
import math
import random 
from Actions import state

def set_sky_color(r, g, b):
    glClearColor(r, g, b, 1.0)

def draw_floor(r, g, b):
    glColor3f(r, g, b)
    glBegin(GL_QUADS)
    glVertex3f(-40, -0.01, -40)
    glVertex3f(40, -0.01, -40)
    glVertex3f(40, -0.01, 40)
    glVertex3f(-40, -0.01, 40)
    glEnd()

def draw_simple_tree(x, z, scale=1.0):
    glPushMatrix()
    glTranslatef(x, 0, z)
    glScalef(scale, scale, scale)
    # Tronco
    glColor3f(0.4, 0.2, 0.1)
    draw_cube(-0.2, 0, -0.2, 0.2, 1.2, 0.2)
    # Copa (dos niveles)
    glColor3f(0.1, 0.5, 0.1)
    draw_cube(-0.8, 1.2, -0.8, 0.8, 2.0, 0.8) # Base de la copa
    glColor3f(0.2, 0.7, 0.2)
    draw_cube(-0.5, 2.0, -0.5, 0.5, 2.8, 0.5) # Punta
    glPopMatrix()

def draw_scenery(scenario_id):
    if scenario_id == 1:   # parque
        set_sky_color(0.4, 0.7, 1.0)
        draw_floor(0.3, 0.7, 0.3)
        for i in range(-25, 26, 8):
            draw_simple_tree(i, -20, 1.2)
            draw_simple_tree(i, 20, 1.0)
            draw_simple_tree(-20, i, 1.1)
            draw_simple_tree(20, i, 0.9)

    elif scenario_id == 2:   # Ccallejon
        set_sky_color(0.01, 0.01, 0.08)
        draw_floor(0.15, 0.15, 0.15)
        # Edificios de fondo (cubos grandes)
        glColor3f(0.1, 0.1, 0.12)
        for x in [-20, -10, 10, 20]:
            draw_cube(x-3, 0, -25, x+3, 10 + (x%3), -15)
        # Farolas con luz
        for z in [-15, 0, 15]:
            glPushMatrix()
            glTranslatef(8, 0, z)
            glColor3f(0.2, 0.2, 0.2)
            draw_cube(-0.2, 0, -0.2, 0.2, 4, 0.2) # Poste
            glColor3f(1.0, 1.0, 0.6) # Luz
            draw_cube(-0.4, 4, -0.4, 0.4, 4.5, 0.4)
            glPopMatrix()

    elif scenario_id == 3:   # teatro
        set_sky_color(0.05, 0.0, 0.1)
        draw_floor(0.6, 0.0, 0.0)
        # Columnas doradas laterales
        glColor3f(0.8, 0.6, 0.2)
        for pos in [(-12, -15), (-12, 0), (12, -15), (12, 0)]:
            draw_cube(pos[0]-0.5, 0, pos[1]-0.5, pos[0]+0.5, 8, pos[1]+0.5)

    elif scenario_id == 4:   #clima de nieve
        set_sky_color(0.7, 0.85, 1.0)
        draw_floor(1.0, 1.0, 1.0)
        for i in range(12):
            x = math.sin(i) * 20
            z = math.cos(i) * 20
            size = 1.0 + (i % 3) * 0.5
            glPushMatrix()
            glTranslatef(x, 0, z)
            glColor3f(0.8, 0.9, 1.0)
            draw_cube(-size, 0, -size, size, size*1.5, size)
            glPopMatrix()

    elif scenario_id == 5:   #volcan
        set_sky_color(0.2, 0.05, 0.0)
        draw_floor(0.1, 0.1, 0.1) # Suelo negro/ceniza
        # Río de lava central
        glColor3f(1.0, 0.3, 0.0)
        draw_cube(-30, -0.02, -5, 30, 0.05, 5)
        # El volcán al fondo
        glColor3f(0.3, 0.2, 0.2)
        draw_cube(-8, 0, -25, 8, 10, -15)
        glColor3f(1.0, 0.5, 0.0) # Lava en la cima
        draw_cube(-3, 10, -22, 3, 10.5, -18)

    elif scenario_id == 6:   # desierto
        set_sky_color(1.0, 0.7, 0.3)
        draw_floor(0.95, 0.8, 0.4)
        for i in range(8):
            x, z = math.sin(i)*15, math.cos(i)*18
            # Cactus con brazos
            glPushMatrix()
            glTranslatef(x, 0, z)
            glColor3f(0.2, 0.5, 0.1)
            draw_cube(-0.3, 0, -0.3, 0.3, 2.5, 0.3) # Tronco
            draw_cube(0.3, 1.2, -0.2, 1.0, 1.5, 0.2) # Brazo
            glPopMatrix()

    elif scenario_id == 7:   # espacio 
        set_sky_color(0.0, 0.0, 0.02)
        draw_floor(0.02, 0.02, 0.05)
        # Estrellas
        glBegin(GL_POINTS)
        for i in range(200):
            glColor3f(1, 1, 1)
            glVertex3f(math.sin(i)*30, 5 + (i%10), math.cos(i)*30)
        glEnd()
        # Meteoritos flotantes
        for i in range(5):
            glColor3f(0.4, 0.4, 0.45)
            x, y, z = -15 + i*7, 3 + (i%2), -10
            draw_cube(x, y, z, x+1.5, y+1.5, z+1.5)

    # Recorre los 3 objetos de colisiones
    for obj in state.objetos_escenas:
        obj.draw()