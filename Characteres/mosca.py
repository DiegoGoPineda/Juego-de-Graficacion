# fox.py
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from Actions import state

def set_mosca_color(r, g, b):
    glColor3f(r, g, b)

def draw_sword(p):
    glPushMatrix()
    glTranslatef(0, 0, -0.6) 
    glRotatef(45, 0, 0, 1)    
    #lighting.set_color(0.4, 0.2, 0.1)
    if p.hay_choque:
        set_mosca_color(*p.color_colision_actual)
    else:   
        set_mosca_color(0.4, 0.2, 0.1)
    glPushMatrix()
    glScalef(0.1, 0.4, 0.1)
    glutSolidCube(1)
    glPopMatrix()
    glTranslatef(0, 0.2, 0)
    glPushMatrix()
    glScalef(0.3, 0.05, 0.15)
    glutSolidCube(1)
    glPopMatrix()
    # hoja de la espada 
    if not p.hay_choque:
        set_mosca_color(0.6, 0.4, 0.2)
    #lighting.set_color(0.6, 0.4, 0.2)
    glTranslatef(0, 0.5, 0)
    glPushMatrix()
    glScalef(0.2, 1.0, 0.08)
    glutSolidCube(1)
    glPopMatrix()
    glPopMatrix()

def draw_box_face(p):
    glDisable(GL_LIGHTING)
    # color basado en colision
    if p.hay_choque:
        glColor3f(1.0,1.0,1.0) # Blanco para resaltar la colisión
    else:
        glColor3f(0.1, 0.1, 0.1) # Color base del hocico
    #lighting.set_color(0.1, 0.1, 0.1)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    for a in range(0, 360, 20):
        rad = math.radians(a)
        glVertex3f(math.cos(rad)*0.2, 0.1 + math.sin(rad)*0.1, 0.51)
    glEnd()
    glBegin(GL_LINE_STRIP)
    points = [(-0.3, -0.2), (-0.2, -0.1), (-0.1, -0.2), (0, -0.1), (0.1, -0.2), (0.2, -0.1), (0.3, -0.2)]
    for px, py in points:
        glVertex3f(px, py, 0.51)
    glEnd()
    glEnable(GL_LIGHTING)

def draw_eyes(p):
    for dx in [-0.22, 0.22]:
        glPushMatrix()
        glTranslatef(dx, 0.1, 0.45)
        set_mosca_color(1, 1, 1) # Blanco para los ojos
        #lighting.set_color(1, 1, 1)
        if p.expression == "blinking": glScalef(1, 0.1, 1)
        elif p.expression == "sad":
            glRotatef(20 if dx > 0 else -20, 0, 0, 1)
            glScalef(1, 0.7, 1)
        elif p.expression == "angry": glRotatef(-30 if dx > 0 else 30, 0, 0, 1)
        elif p.expression == "shouting": glScalef(1.2, 1.2, 1)
        glutSolidSphere(0.2, 20, 20)
        if p.expression in ["surprised", "shouting"]:
            #lighting.set_color(0, 0, 0)
            glTranslatef(0, 0, 0.16)
            glutSolidSphere(0.06, 10, 10)
        glPopMatrix()

def draw_mouth(p):
    glDisable(GL_LIGHTING)
    glLineWidth(3)
    set_mosca_color(1, 1, 1) # Blanco para la boca
    #  lighting.set_color(1, 1, 1)
    for dx in [-0.1, 0.1]:
        glPushMatrix()
        glTranslatef(dx, -0.2, 0.52)
        glRotatef(180, 1, 0, 0)
        glutSolidCone(0.04, 0.1, 10, 10)
        glPopMatrix()
    if p.expression == "happy":
        set_mosca_color(1, 0.2, 0.2) # Rojo para feliz
        #lighting.set_color(1, 0.2, 0.2)
        glBegin(GL_LINE_STRIP)
        for a in range(210, 330, 10):
            rad = math.radians(a)
            glVertex3f(math.cos(rad)*0.25, -0.15 + math.sin(rad)*0.1, 0.53)
        glEnd()
    elif p.expression == "sad":
        set_mosca_color(0.2, 0.2, 1) # Azul para triste
        #lighting.set_color(0.2, 0.2, 1)
        glBegin(GL_LINE_STRIP)
        for a in range(30, 150, 10):
            rad = math.radians(a)
            glVertex3f(math.cos(rad)*0.25, -0.3 + math.sin(rad)*0.1, 0.53)
        glEnd()
    elif p.expression == "shouting":
        set_mosca_color(0, 0, 0) #  Negro para gritando
        #lighting.set_color(0, 0, 0)
        glPushMatrix()
        glTranslatef(0, -0.25, 0.51)
        glScalef(1, 1.2, 1)
        glutSolidSphere(0.12, 20, 20)
        glPopMatrix()
    glEnable(GL_LIGHTING)

def draw_mosca_full(p):
    quad = gluNewQuadric()
    glPushMatrix()   
    glTranslatef(0, 1.65, 0) # pa que no este abajo
    # --- LÓGICA DE LAS 7 ACCIONES ---
    if p.walking:
        glTranslatef(0, abs(math.sin(p.animation_angle))*0.1, 0)
    
    if p.reaction_type == "jump":
        jump_h = math.sin(math.pi * p.reaction_timer / p.reaction_duration) * 1.5
        glTranslatef(0, jump_h, 0)
    elif p.reaction_type == "spin":
        glRotatef(360 * (p.reaction_timer / p.reaction_duration), 0, 1, 0)
    elif p.reaction_type == "flip": # NUEVA: Mortal
        angle = ( p.reaction_timer / p.reaction_duration) * 360
        jump_h = math.sin(math.pi * p.reaction_timer / p.reaction_duration) * 1.8
        glTranslatef(0, jump_h, 0)
        glRotatef(angle, 1, 0, 0)
    #elif p.current_movement == "nod": # NUEVA: Asentir (cabeceo)
        #glRotatef(math.sin(p.movement_timer * 0.4) * 20, 1, 0, 0)
    elif p.reaction_type == "grow": # NUEVA: Crecer
        s = 1.0 + math.sin(math.pi * p.reaction_timer / p.reaction_duration) * 0.6
        glScalef(s, s, s)

    # Cuerpo (Caja)
    glPushMatrix()
    if p.hay_choque:
        set_mosca_color(*p.color_colision_actual)
    else:
        set_mosca_color(0.7, 0.55, 0.35)
    #lighting.set_color(0.7, 0.55, 0.35) 
    glScalef(1.1, 1.2, 0.9)
    glutSolidCube(1)
    draw_box_face(p)
    glPopMatrix()
    
    # Cuello
    glPushMatrix()
    glTranslatef(0, 0.6, 0)
    glRotatef(90, 1, 0, 0)
    set_mosca_color(0.1, 0.1, 0.1) #color del cuello
    #  lighting.set_color(0.1, 0.1, 0.1)
    gluCylinder(quad, 0.1, 0.1, 0.2, 10, 10)
    glPopMatrix()

    draw_sword(p)

    # Cabeza (Esfera Negra)
    glPushMatrix()
    glTranslatef(0, 1.25, 0)
    set_mosca_color(0.08, 0.08, 0.08) # color de la cabeza
    #lighting.set_color(0.08, 0.08, 0.08)
    glutSolidSphere(0.55, 30, 30)
    draw_eyes(p)
    draw_mouth(p)
    # Cuernos
    set_mosca_color(0.5, 0.1, 0.8) # color de los cuernos
    #lighting.set_color(0.5, 0.1, 0.8) 
    for dx in [-0.4, 0.4]:
        glPushMatrix()
        glTranslatef(dx, 0.35, 0) 
        glRotatef(-45 if dx > 0 else 45, 0, 0, 1)
        glutSolidCone(0.18, 0.6, 20, 20)
        glPopMatrix()
    glPopMatrix()

    # Extremidades (Piernas y Brazos)
    # Piernas
    for dx in [-0.3, 0.3]:
        glPushMatrix()
        glTranslatef(dx, -0.65, 0)
        if p.walking:
            glRotatef(math.sin(p.animation_angle)*30 * (1 if dx>0 else -1), 1, 0, 0)
        set_mosca_color(0.1, 0.1, 0.1) # color de las piernas
        #lighting.set_color(0.1, 0.1, 0.1)
        glRotatef(90, 1, 0, 0)
        gluCylinder(quad, 0.08, 0.08, 0.7, 15, 15)
        glTranslatef(0, 0, 0.7)
        set_mosca_color(0.65, 0.45, 0.25) # color de los pies   
        #lighting.set_color(0.65, 0.45, 0.25)
        glPushMatrix(); glScalef(0.4, 0.3, 0.6); glutSolidCube(1); glPopMatrix()
        glPopMatrix()

    # Brazos
    for dx in [-0.7, 0.7]:
        glPushMatrix()
        glTranslatef(dx, 0.2, 0)
        if p.expression == "wave" and dx < 0:
            glRotatef(-150 + math.sin(p.animation_angle*0.2)*20, 0, 0, 1)
        elif p.expression == "dance":
            glRotatef(math.sin(p.animation_angle*0.2)*40, 0, 0, 1)
        set_mosca_color(0.1, 0.1, 0.1) # color de los brazos    
        #lighting.set_color(0.1, 0.1, 0.1)
        glRotatef(90, 1, 0, 0)
        gluCylinder(quad, 0.07, 0.07, 0.7, 15, 15)
        glPopMatrix()

    glPopMatrix()
