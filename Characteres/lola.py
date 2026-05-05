from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from Actions import state 
from Utils.dibujar_cubo import draw_cube
from Actions.luz import set_color

def get_collision_color(p):
    
    return getattr(p, 'color_colision_actual', (1.0, 1.0, 1.0))

def draw_body(p):
    glPushMatrix()
    if p.hay_choque:
        set_color(*get_collision_color(p))
    else:
        set_color(0.95, 0.9, 0.8)
    # Color Crema para el cuerpo
    draw_cube(0, 0, 1, 3, 1, 2)
    glPopMatrix()

def draw_head(p):
    glPushMatrix()
    if p.hay_choque:
        set_color(*get_collision_color(p))
    else:
        set_color(0.95, 0.9, 0.8)
    # Cabeza base (Seal Point)
    draw_cube(3, 0, 1.5, 4, 1, 2.5)   

    # Color base oscuro
    if p.expression == "angry":
        set_color(0.6, 0.0, 0.0) # Rojo si está enojado
    else:
        set_color(0.2, 0.15, 0.1)
  
    y_min, y_max = 0.35, 0.65
    z_min, z_max = 1.6, 2.1 # Basado en el original (1.5 a 2) pero centrado

    if p.expression == "happy":
        # Desplazamos el bloque hacia arriba
        z_min += 0.2; z_max += 0.2
    elif p.expression == "sad":
        # Desplazamos el bloque hacia abajo
        z_min -= 0.1; z_max -= 0.1
    elif p.expression == "surprised":
        # Se vuelve un cubo mas pequeño (boca abierta)
        y_min, y_max = 0.45, 0.55
        z_min, z_max = 1.7, 1.9
    elif p.expression == "fear":
        # Se vuelve una línea ancha
        y_min, y_max = 0.2, 0.8
        z_min, z_max = 1.75, 1.85
    elif p.expression == "interest":
        # Ladeado
        y_min += 0.05; y_max += 0.1

    # Dibujamos el hocico con la profundidad del original (4.35)
    draw_cube(4, y_min, z_min, 4.35, y_max, z_max)
    
    glPopMatrix()

def draw_eyes(p):
    is_blinking = math.sin(p.blink_timer) > 0.95
    
    for dy in [0.1, 0.7]:
        glPushMatrix()
        
        # Colores dinámicos según expresión
        if p.expression == "angry": 
            set_color(1.0, 0.0, 0.0)
        elif p.expression == "surprised": 
            set_color(1.0, 1.0, 1.0)
        elif p.expression == "fear": 
            set_color(1.0, 1.0, 0.0) # Amarillo
        else: 
            set_color(0.0, 0.6, 1.0) # Azul original

        # Formas de los ojos
        if p.expression == "wink" and dy == 0.1:
            # Ojo izquierdo cerrado para el guiño
            draw_cube(4.01, dy, 2.05, 4.05, dy+0.2, 2.1)
        elif p.expression == "interest":
            # Un ojo más grande que otro
            size = 0.25 if dy == 0.1 else 0.15
            draw_cube(4.01, dy, 2, 4.05, dy+size, 2.2)
        elif is_blinking:
            # Parpadeo normal
            draw_cube(4.01, dy, 2.05, 4.05, dy+0.2, 2.1)
        else:
            # Ojo normal
            draw_cube(4.01, dy, 2, 4.05, dy+0.2, 2.2)
            
        glPopMatrix()
def draw_ears(p):
    glPushMatrix()
    set_color(0.2, 0.15, 0.1)
    
    # Movimiento de orejas según expresión
    z_off = 0
    if p.expression == "angry": z_off = -0.2 # Orejas gachas (ira)
    if p.expression == "surprised": z_off = 0.1 # Orejas alerta
    
    draw_cube(3.1, 0.1, 2.5 + z_off, 3.4, 0.3, 2.75 + z_off)
    draw_cube(3.1, 0.7, 2.5 + z_off, 3.4, 0.9, 2.75 + z_off)
    glPopMatrix()

def draw_legs(p):
    glPushMatrix()
    set_color(0.25, 0.2, 0.15) 
    
    # patas izquierda
    glPushMatrix()
    glTranslate(0, 0, 0.5) 
    glRotate(p.leg_swing, 0, 1, 0) 
    glTranslate(0, 0, -0.5) 
    draw_cube(0, 0, 0, 0.5, 0.5, 1)   # Pata 1
    draw_cube(2.5, 0, 0, 3, 0.5, 1)   # Pata 3
    glPopMatrix()

    # patas derecha
    glPushMatrix()
    glTranslate(0, 1.0, 0.5) 
    glRotate(-p.leg_swing, 0, 1, 0)
    glTranslate(0, -1.0, -0.5) 
    draw_cube(0, 0.5, 0, 0.5, 1, 1)   # Pata 2
    draw_cube(2.5, 0.5, 0, 3, 1, 1)   # Pata 4
    glPopMatrix()
    
    glPopMatrix()

def draw_tail(p):
    glPushMatrix()
    set_color(0.2, 0.15, 0.1)
    angle = math.sin(p.tail_angle) * 15 # Aumentamos un poco el rango
    
    # Pivote en la base de la cola
    glTranslate(0, 0.5, 1.8)
    glRotate(angle, 0, 1, 0)
    glTranslate(0, -0.5, -1.8)
    
    draw_cube(-2.5, 0.37, 1.75, 0, 0.62, 2)
    glPopMatrix()

def draw_gato_full(p):
    glPushMatrix()
    
    # Rotación según dirección de movimiento
    glRotatef(p.direction_angle, 0, 1, 0)
    
    # reaciones
    if p.reaction_type == "jump":
        # Salto parabólico usando el timer de reacción
        z_offset = math.sin(math.pi * p.reaction_timer / p.reaction_duration) * 1.5
        glTranslatef(0, 0, z_offset) 
    elif p.reaction_type == "spin":
        # Giro completo de 360 grados
        angle = 360 * (p.reaction_timer / p.reaction_duration)
        glRotatef(angle, 0, 0, 1)
    elif p.reaction_type == "shake":
        # Vibración rápida (ira o miedo)
        x_offset = math.sin(p.reaction_timer * 2.0) * 0.1
        glTranslatef(x_offset, 0, 0)

    # Centrar el modelo
    glRotatef(-90, 0, 1, 0)
    glRotatef(-90, 1, 0, 0)
    glTranslatef(-1.5, -0.5, 0)

    # Dibujar partes
    draw_body(p)
    draw_head(p)
    draw_ears(p)
    draw_eyes(p)
    draw_legs(p)
    draw_tail(p) 
    glPopMatrix()