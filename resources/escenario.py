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

# --- NUEVOS ELEMENTOS DE ESCENARIO ---

def draw_scenery(scenario_id):
    t = time.time() # Para animaciones sutiles

    if scenario_id == 1:   # CIUDAD FUTURISTA (Tron Style)
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

    elif scenario_id == 2:   # JARDÍN ZEN (Minimalista Japones)
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

    elif scenario_id == 3:   # MINA DE CRISTALES (Cueva)
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

    elif scenario_id == 4:   # ISLA FLOTANTE (Cielo despejado)
        set_sky_color(0.4, 0.8, 1.0)
        draw_floor(0.3, 0.8, 0.3)
        # Cascadas de cubos (nubes bajas)
        for i in range(10):
            glColor3f(1, 1, 1)
            cx, cz = math.sin(i)*45, math.cos(i)*45
            draw_cube(cx, -5, cz, cx+5, -2, cz+5)
        # Árboles estilizados (Copa cuadrada grande)
        glColor3f(0.5, 0.3, 0.1)
        draw_cube(-2, 0, -20, 2, 8, -16)
        glColor3f(0.1, 0.7, 0.1)
        draw_cube(-6, 8, -24, 6, 16, -12)

    elif scenario_id == 5:   # LABORATORIO DE ENERGÍA
        set_sky_color(0.1, 0.1, 0.1)
        draw_floor(0.3, 0.3, 0.3) # Metal
        # Bobinas de Tesla / Pilares de energía
        pulse = (math.sin(t * 5) + 1) / 2
        for x in [-20, 20]:
            glColor3f(0.4, 0.4, 0.4)
            draw_cube(x-2, 0, -5, x+2, 12, 5)
            glColor3f(1.0 * pulse, 1.0, 0.0) # Rayo amarillo pulsante
            draw_cube(x-0.5, 12, -0.5, x+0.5, 20, 0.5)

    elif scenario_id == 6:   # DIMENSIÓN DE ERROR (Glitched)
        set_sky_color(0.0, 0.0, 0.0)
        draw_floor(0.1, 0.0, 0.1)
        # Cubos de colores aleatorios volando
        for i in range(15):
            x = math.sin(t + i) * 30
            y = 5 + math.cos(i) * 5
            z = math.cos(t + i) * 30
            if i % 2 == 0: glColor3f(1, 0, 0.3)
            else: glColor3f(0, 1, 0.3)
            draw_cube(x, y, z, x+2, y+2, z+2)

    elif scenario_id == 7:   # OCÉANO DE DATOS (Abismo)
        set_sky_color(0.0, 0.1, 0.2)
        draw_floor(0.0, 0.2, 0.4)
        # Pilares que suben y bajan (como un ecualizador)
        for i in range(-30, 31, 10):
            h = 4 + math.sin(t + i) * 3
            glColor3f(0.0, 0.5, 0.8)
            draw_cube(i-2, 0, -35, i+2, h, -31)
            draw_cube(i-2, 0, 31, i+2, h, 35)

    # Dibujar objetos con colisión
    for obj in state.objetos_escenas:
        obj.draw()