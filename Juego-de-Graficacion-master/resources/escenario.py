from OpenGL.GL import *
from Characteres.gato import draw_cube  
import math
import time
from Actions import state

def set_sky_color(r, g, b):
    glClearColor(r, g, b, 1.0)

def draw_floor(r, g, b):
    glColor3f(r, g, b)
    glBegin(GL_QUADS)
    glVertex3f(-60, -0.01, -60)
    glVertex3f(60, -0.01, -60)
    glVertex3f(60, -0.01, 60)
    glVertex3f(-60, -0.01, 60)
    glEnd()

def draw_scenery(scenario_id):
    t = time.time() # Para animaciones sutiles
    if scenario_id == 1:   # ciudad futuro
        set_sky_color(0.0, 0.0, 0.1) # Azul muy oscuro
        draw_floor(0.1, 0.1, 0.2)
        # Rejilla luminosa en el suelo
        glColor3f(0.0, 1.0, 1.0)
        for i in range(-50, 51, 10):
            draw_cube(i, -0.01, -50, i+0.1, 0.02, 50)
            draw_cube(-50, -0.01, i, 50, 0.02, i+0.1)
        # Edificios con bordes brillantes
        for x, z in [(-30, -30), (30, -30), (-30, 30), (30, 30)]:
            glColor3f(0.1, 0.1, 0.3)
            draw_cube(x-5, 0, z-5, x+5, 20, z+5)
            glColor3f(0.0, 0.8, 1.0) # Detalle luz
            draw_cube(x-5.1, 18, z-5.1, x+5.1, 19, z+5.1)

    elif scenario_id == 2:   # Jjardin
        set_sky_color(0.8, 0.9, 1.0) # Blanco azulado
        draw_floor(0.9, 0.9, 0.8) # Arena clara
        # Piedras decorativas
        glColor3f(0.4, 0.4, 0.4)
        draw_cube(-15, 0, -10, -5, 4, -2)
        draw_cube(10, 0, 5, 14, 2, 9)
        # Un arco Torii simple al fondo
        glColor3f(0.8, 0.1, 0.1)
        draw_cube(-10, 0, -40, -8, 15, -38) # Pilar L
        draw_cube(8, 0, -40, 10, 15, -38)  # Pilar R
        draw_cube(-12, 13, -41, 12, 15, -37) # Techo
    elif scenario_id == 3:   # cueva
        set_sky_color(0.05, 0.02, 0.1)
        draw_floor(0.1, 0.05, 0.15)
        # Cristales que "crecen" del suelo
        for i in range(8):
            ang = i * 45
            x, z = math.cos(ang)*20, math.sin(ang)*20
            h = 5 + math.sin(t + i)*2 # Animación de levitación
            glColor3f(0.6, 0.0, 1.0) # Púrpura brillante
            draw_cube(x-1, 0, z-1, x+1, h, z+1)
            glColor3f(1, 0.5, 1) # Punta brillante
            draw_cube(x-0.5, h, z-0.5, x+0.5, h+1, z+0.5)
    elif scenario_id == 4:   # Salón de clases
        set_sky_color(0.95, 0.95, 0.9)
        draw_floor(0.78, 0.65, 0.43)
        # Paredes y techo
        glColor3f(0.86, 0.86, 0.78)
        draw_cube(-40, 0, -40, 40, 20, -39)
        draw_cube(-40, 0, 39, 40, 20, 40)
        draw_cube(-40, 0, -40, -39, 20, 40)
        draw_cube(39, 0, -40, 40, 20, 40)
        # Ventanas grandes a la derecha
        glColor3f(0.7, 0.9, 1.0)
        for i in range(3):
            z = -25 + i * 18
            draw_cube(38.5, 6, z, 39.5, 14, z+10)
            glColor3f(0.4, 0.4, 0.6)
            draw_cube(38.2, 6, z, 38.5, 14, z+10)
        # Pizarrón frontal
        glColor3f(0.05, 0.05, 0.05)
        draw_cube(-20, 5, -39.5, 20, 15, -38.5)
        glColor3f(0.85, 0.85, 0.3)
        draw_cube(-19.5, 5.5, -39.4, -5, 6.5, -39.3)
        draw_cube(-4.5, 5.5, -39.4, 4.5, 6.5, -39.3)
        draw_cube(5, 5.5, -39.4, 19.5, 6.5, -39.3)
        # Plataformas de inicio del nivel 1
        if state.level1_enabled and state.level1_phase == state.LEVEL1_WAITING:
            for x, z, width, depth in state.level1_platforms:
                glColor3f(0.1, 0.6, 0.1)
                half_w, half_d = width / 2, depth / 2
                draw_cube(x - half_w, 0, z - half_d, x + half_w, 0.8, z + half_d)
                glColor3f(0.9, 0.9, 0.2)
                draw_cube(x - half_w + 0.2, 0.8, z - half_d + 0.2, x + half_w - 0.2, 1.0, z + half_d - 0.2)
        # Escritorio del profesor y silla
        glColor3f(0.45, 0.3, 0.15)
        draw_cube(-6, 0, -30, 6, 2, -26)
        draw_cube(-4.5, 0, -34, -2, 3, -32)
        # Mesas de estudiantes (se ocultan cuando el nivel 1 ya comenzó)
        if not (state.level1_enabled and state.level1_phase >= state.LEVEL1_ACTIVE):
            for fila in range(4):
                for col in range(4):
                    x = -28 + col * 16
                    z = -10 + fila * 10
                    glColor3f(0.55, 0.35, 0.18)
                    draw_cube(x, 0, z, x+8, 1.2, z+5)
                    glColor3f(0.4, 0.25, 0.14)
                    draw_cube(x+1, 0, z-2, x+4, 2.2, z-1)
        # Carteles y reloj
        glColor3f(0.9, 0.4, 0.2)
        draw_cube(-38.5, 12, 10, -35, 16, 14)
        draw_cube(-38.5, 12, -30, -35, 16, -26)
        glColor3f(0.2, 0.2, 0.2)
        draw_cube(30, 14, 10, 33, 17, 13)
    elif scenario_id == 5:   # Cancha de fútbol
        set_sky_color(0.52, 0.8, 1.0)
        draw_floor(0.15, 0.55, 0.15)
        glColor3f(1, 1, 1)
        draw_cube(-40, 0.01, -20, -38, 0.02, 20)
        draw_cube(38, 0.01, -20, 40, 0.02, 20)
        draw_cube(-40, 0.01, -20, 40, 0.02, -18)
        draw_cube(-40, 0.01, 18, 40, 0.02, 20)
        draw_cube(-1, 0.01, -20, 1, 0.02, 20)
        for ang in range(0, 360, 10):
            rad = 8
            x = math.cos(math.radians(ang)) * rad
            z = math.sin(math.radians(ang)) * rad
            draw_cube(x-0.2, 0.01, z-0.2, x+0.2, 0.02, z+0.2)
        for side in [-1, 1]:
            draw_cube(side * 30, 0.01, -9, side * 35, 0.02, 9)
            draw_cube(side * 30, 0.01, -2, side * 32, 0.02, 2)
        glColor3f(1, 1, 1)
        for side in [-1, 1]:
            draw_cube(side * 35, 0, -3, side * 36, 3, 3)
            draw_cube(side * 35, 3, -3, side * 36, 4, -1)
            draw_cube(side * 35, 3, 1, side * 36, 4, 3)
        glColor3f(0.4, 0.4, 0.4)
        for x in range(-35, 36, 10):
            draw_cube(x, 0, 22, x+6, 3, 24)
            draw_cube(x, 0, -24, x+6, 3, -22)
        glColor3f(0.8, 0.2, 0.1)
        draw_cube(-5, 0, 25, 5, 10, 26)
        glColor3f(0.9, 0.9, 0.2)
        draw_cube(-4.5, 10, 25.5, 4.5, 12, 25.7)
        for x in [-35, 35]:
            glColor3f(0.7, 0.7, 0.7)
            draw_cube(x, 0, 25, x+1, 12, 25.5)
            glColor3f(1, 1, 0.8)
            draw_cube(x-1, 12, 25.2, x+2, 14, 25.3)
    elif scenario_id == 6:   # Auditorio de graduaciones
        set_sky_color(0.7, 0.7, 0.78)
        draw_floor(0.55, 0.55, 0.55)
        glColor3f(0.3, 0.2, 0.15)
        draw_cube(-20, 0, -50, 20, 3, -40)
        glColor3f(0.6, 0.1, 0.1)
        draw_cube(-25, 3, -51, 25, 18, -49)
        glColor3f(0.45, 0.25, 0.1)
        draw_cube(-1.5, 3, -45, 1.5, 7, -43)
        draw_cube(-2, 0, -46, 2, 3, -44)
        glColor3f(0.55, 0.1, 0.1)
        draw_cube(-8, 0.01, -10, 8, 0.02, 0)
        for fila in range(8):
            z = 2 + fila * 4
            for col in range(-8, 9, 4):
                glColor3f(0.25, 0.25, 0.3)
                draw_cube(col, 0, z, col+3, 1.2, z+2)
                glColor3f(0.2, 0.2, 0.25)
                draw_cube(col, 1.2, z, col+3, 2.2, z+2)
        glColor3f(0.9, 0.9, 0.1)
        draw_cube(-18, 0, -38, -17, 10, -37)
        draw_cube(17, 0, -38, 18, 10, -37)
        glColor3f(0.85, 0.85, 0.85)
        draw_cube(-18.5, 10, -38.5, -16.5, 13, -38)
        draw_cube(16.5, 10, -38.5, 18.5, 13, -38)
    elif scenario_id == 7:   # océano profundo
        set_sky_color(0.0, 0.1, 0.2)
        draw_floor(0.0, 0.2, 0.4)
        for i in range(-30, 31, 10):
            h = 4 + math.sin(t + i) * 3
            glColor3f(0.0, 0.5, 0.8)
            draw_cube(i-2, 0, -35, i+2, h, -31)
    
    # Dibujar objetos con colisión solo en escenarios libres (no en niveles)
    if scenario_id not in [4, 5, 6]:
        for obj in state.objetos_escenas:
            obj.draw()