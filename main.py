from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from resources import escenario
from Actions import state, camera, update, gestor_audio, luz
from Characteres import gato, lola, mosca, KingLi, amongus, meteoro
from resources import input_handlers, grid
import math

def init():
    glEnable(GL_DEPTH_TEST) 
    glEnable(GL_LIGHTING) 
    glEnable(GL_LIGHT0)      
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_NORMALIZE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    luz.setup_lighting() # Configuramos los componentes de la luz una vez
    glClearColor(0.05, 0.05, 0.1, 1.0)

def draw_text(x, y, text, font=GLUT_BITMAP_8_BY_13, color=(0,0,0)):
    glDisable(GL_LIGHTING)
    glColor3f(*color)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))
    glEnable(GL_LIGHTING)

def draw_stroke_text(x, y, text, scale=0.3, color=(1,1,1), line_width=2.0):
    # estilo para titulos
    glDisable(GL_LIGHTING)
    glColor3f(*color)
    glLineWidth(line_width)
    glPushMatrix()
    glTranslatef(x, y, 0)
    glScalef(scale, scale, 1.0) # escalacion de la fuente
    for char in text:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))
    glPopMatrix()
    glLineWidth(1.0) # Restauramos el grosor normal
    glEnable(GL_LIGHTING)

def draw_stats_bar(x, y, label, value, max_value=10, color=(0, 1, 0)):
    #titulo 
    draw_text(x, y + 4, label, GLUT_BITMAP_HELVETICA_12, (1, 1, 1))
    # ui
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND) # brillo para la barra
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # Configuración de dimensions
    offset_x = 100  # Espacio para el texto
    ancho_total = 200
    alto = 12
    ancho_relleno = ancho_total * (value / max_value)
    # fondo
    glBegin(GL_QUADS)
    glColor4f(0.05, 0.05, 0.05, 0.8) # Casi negro
    glVertex2f(x + offset_x, y)
    glVertex2f(x + offset_x + ancho_total, y)
    glColor4f(0.15, 0.15, 0.15, 0.8) # Un poco más claro arriba
    glVertex2f(x + offset_x + ancho_total, y + alto)
    glVertex2f(x + offset_x, y + alto)
    glEnd()
    glBegin(GL_QUADS)
    # Color base más oscuro en la parte inferior
    glColor3f(color[0] * 0.4, color[1] * 0.4, color[2] * 0.4)
    glVertex2f(x + offset_x, y)
    glVertex2f(x + offset_x + ancho_relleno, y)
    # Color brillante en la parte superior
    glColor3f(color[0], color[1], color[2])
    glVertex2f(x + offset_x + ancho_relleno, y + alto)
    glVertex2f(x + offset_x, y + alto)
    glEnd()
    glBegin(GL_QUADS)
    glColor4f(1.0, 1.0, 1.0, 0.2) # Blanco muy suave
    glVertex2f(x + offset_x, y + (alto / 2))
    glVertex2f(x + offset_x + ancho_relleno, y + (alto / 2))
    glColor4f(1.0, 1.0, 1.0, 0.0) # Desvanece a transparente
    glVertex2f(x + offset_x + ancho_relleno, y + alto)
    glVertex2f(x + offset_x, y + alto)
    glEnd()
    glLineWidth(1.0)
    glBegin(GL_LINE_LOOP)
    glColor4f(1.0, 1.0, 1.0, 0.3) # Borde blanco tenue
    glVertex2f(x + offset_x, y)
    glVertex2f(x + offset_x + ancho_total, y)
    glVertex2f(x + offset_x + ancho_total, y + alto)
    glVertex2f(x + offset_x, y + alto)
    glEnd()
    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

def draw_players():
    # Jugador 1
    glPushMatrix()
    glTranslatef(state.p1.x, state.p1.y + state.p1.jump_offset + state.p1.walk_bob, state.p1.z)
    if state.p1.tipo == "gato": gato.draw_gato_full(state.p1)
    elif state.p1.tipo == "mosca": mosca.draw_mosca_full(state.p1)
    elif state.p1.tipo == "lola": lola.draw_gato_full(state.p1)
    elif state.p1.tipo == "KingLi": KingLi.draw_kingli_full(state.p1)
    elif state.p1.tipo == "amongus": amongus.draw_amongus_full(state.p1)
    elif state.p1.tipo == "meteoro": meteoro.draw_metetoro_full(state.p1)
    glPopMatrix()
    # Jugador 2
    glPushMatrix()
    glTranslatef(state.p2.x, state.p2.y + state.p2.jump_offset + state.p2.walk_bob, state.p2.z)
    if state.p2.tipo == "gato": gato.draw_gato_full(state.p2)
    elif state.p2.tipo == "mosca": mosca.draw_mosca_full(state.p2)
    elif state.p2.tipo == "lola": lola.draw_gato_full(state.p2)
    elif state.p2.tipo == "KingLi": KingLi.draw_kingli_full(state.p2)
    elif state.p2.tipo == "amongus": amongus.draw_amongus_full(state.p2)
    elif state.p2.tipo == "meteoro": meteoro.draw_metetoro_full(state.p2)
    glPopMatrix()

def draw_ittol_logo(x, y, radius, angle=0.0):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glRotatef(angle, 0, 0, 1)
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    # 1. Dientes del engrane azul 
    glColor3f(0.0, 0.2, 0.6) # Azul Tec
    for i in range(12):
        glPushMatrix()
        glRotatef(i * 30, 0, 0, 1) # 12 dientes 
        glBegin(GL_QUADS)
        glVertex2f(-radius * 0.15, radius * 0.8)
        glVertex2f(radius * 0.15, radius * 0.8)
        glVertex2f(radius * 0.1, radius * 1.15)
        glVertex2f(-radius * 0.1, radius * 1.15)
        glEnd()
        glPopMatrix()
    # base del engrane
    glBegin(GL_POLYGON)
    for i in range(36):
        theta = 2.0 * math.pi * i / 36
        glVertex2f(radius * math.cos(theta), radius * math.sin(theta))
    glEnd()
    # centro
    glColor3f(0.0, 0.7, 0.3)
    glBegin(GL_POLYGON)
    for i in range(36):
        theta = 2.0 * math.pi * i / 36
        glVertex2f(radius * 0.65 * math.cos(theta), radius * 0.65 * math.sin(theta))
    glEnd()  
    # hueco
    glColor3f(0.02, 0.05, 0.12)
    glBegin(GL_POLYGON)
    for i in range(36):
        theta = 2.0 * math.pi * i / 36
        glVertex2f(radius * 0.3 * math.cos(theta), radius * 0.3 * math.sin(theta))
    glEnd() 
    glPopMatrix()

def draw_arcade_stars(y_pos, tiempo_ms):
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)   
    colores = [(1.0, 0.2, 0.6), (0.0, 0.8, 1.0), (1.0, 0.9, 0.0)]  
    start_x = 120  
    espaciado = 40   
    for i in range(15):
        x = start_x + (i * espaciado)
        color_idx = int((tiempo_ms / 150) + i) % 3 
        glColor3f(*colores[color_idx])    
        glPushMatrix()
        glTranslatef(x, y_pos, 0)
        glRotatef(45, 0, 0, 1) 
        glBegin(GL_QUADS)
        glVertex2f(-6, -6); glVertex2f(6, -6)
        glVertex2f(6, 6); glVertex2f(-6, 6)
        glEnd()
        glPopMatrix()       
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

def draw_main_menu():
    glClearColor(0.02, 0.05, 0.12, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glColor3f(1.0, 0.4, 0.0) 
    glBegin(GL_QUADS)
    glVertex2f(0, 580); glVertex2f(800, 580)
    glVertex2f(800, 600); glVertex2f(0, 600)
    glEnd()
    glLineWidth(3.0)
    glColor3f(0.0, 0.4, 0.8) 
    glBegin(GL_LINES)
    glVertex2f(0, 475); glVertex2f(800, 475)
    glVertex2f(0, 465); glVertex2f(800, 465)
    glEnd()
    tiempo_actual = glutGet(GLUT_ELAPSED_TIME)
    draw_ittol_logo(400, 280, 120, angle=tiempo_actual * 0.02)
    glDisable(GL_DEPTH_TEST)
    draw_arcade_stars(560, tiempo_actual)
    draw_arcade_stars(60, tiempo_actual)
    texto_titulo = "CONOCE-TEC"
    draw_stroke_text(165, 490, texto_titulo, scale=0.5, color=(1, 1, 1), line_width=4.0)
    texto_sub = "CONOCE EL NIDO"
    draw_stroke_text(265, 425, texto_sub, scale=0.2, color=(1.0, 0.6, 0.0), line_width=2.5)
    opciones = ["JUGAR", "MUNDO LIBRE", "SALIR"]
    for i, texto in enumerate(opciones):
        y_base = 320 - (i * 100)  
        glDisable(GL_LIGHTING)
        if i == state.indice_boton:
            glColor3f(0.0, 0.3, 0.7) 
            glBegin(GL_QUADS)
            glVertex2f(270, y_base - 5); glVertex2f(530, y_base - 5)
            glVertex2f(530, y_base + 55); glVertex2f(270, y_base + 55)
            glEnd() 
            glColor3f(1.0, 0.6, 0.0) 
            glLineWidth(4.0) 
            glBegin(GL_LINE_LOOP)
            glVertex2f(270, y_base - 5); glVertex2f(530, y_base - 5)
            glVertex2f(530, y_base + 55); glVertex2f(270, y_base + 55)
            glEnd()  
            glBegin(GL_TRIANGLES)
            glVertex2f(230, y_base + 25); glVertex2f(260, y_base + 40); glVertex2f(260, y_base + 10)
            glVertex2f(570, y_base + 25); glVertex2f(540, y_base + 40); glVertex2f(540, y_base + 10)
            glEnd()
            color_texto = (1, 1, 1) 
        else:
            glColor3f(0.05, 0.05, 0.08)
            glBegin(GL_QUADS)
            glVertex2f(280, y_base); glVertex2f(520, y_base)
            glVertex2f(520, y_base + 50); glVertex2f(280, y_base + 50)
            glEnd()
            glColor3f(0.2, 0.2, 0.3)
            glLineWidth(1.0)
            glBegin(GL_LINE_LOOP)
            glVertex2f(280, y_base); glVertex2f(520, y_base)
            glVertex2f(520, y_base + 50); glVertex2f(280, y_base + 50)
            glEnd() 
            color_texto = (0.4, 0.4, 0.4) 
        glDisable(GL_DEPTH_TEST)
        x_btn = 362 if texto == "JUGAR" else 368
        draw_text(x_btn, y_base + 20, texto, GLUT_BITMAP_HELVETICA_18, color_texto)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING) 
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def show_game_instructions():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    instructions = [
        "Controles:",
        "P1: WASD | P2: FLECHAS",
        "ESC: Menu Principal",
        "1-7: Escenarios",
        "0: Ocultar ayuda"
    ]
    y_pos = 570
    for line in instructions:
        draw_text(20, y_pos, line, color=(1,1,1))
        y_pos -= 20
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_multijugador_menu():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    stats = {
        "gato": {"nombre": "Timoteo", "vel": 9, "fza": 3, "salto": 8},
        "lola": {"nombre": "Lola", "vel": 4, "fza": 3, "salto": 5},
        "mosca": {"nombre": "Cartonix", "vel": 6, "fza": 6, "salto": 6},
        "KingLi": {"nombre": "King-Lee", "vel": 8, "fza": 8, "salto": 8},
        "amongus": {"nombre": "Among Us", "vel": 5, "fza": 5, "salto": 5},
        "meteoro": {"nombre": "Meteoro", "vel": 7, "fza": 7, "salto": 6}
    }
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800/600, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    cam_x = (state.indice_menu - 2.5) * 5.5
    gluLookAt(cam_x, 1.5, 15, cam_x, 0, 0, 0, 1, 0) 
    glEnable(GL_LIGHTING)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.8, 0.8, 0.8, 1.0]) 
    luz.apply_light_position() 
    
    for i, p in enumerate(state.personajes_pool):
        glPushMatrix()
        x_pos = (i - 2.5) * 5.5 
        glTranslatef(x_pos, -2.0, 0)
        if i == state.indice_menu:
            bobbing = math.sin(glutGet(GLUT_ELAPSED_TIME) * 0.005) * 0.2
            glTranslatef(0, bobbing, 0)
            glScalef(1.4, 1.4, 1.4) 
            glRotatef(glutGet(GLUT_ELAPSED_TIME) * 0.08, 0, 1, 0)
        else:
            glScalef(0.7, 0.7, 0.7)
            glColor3f(0.4, 0.4, 0.4) 
        
        if p.tipo == "gato": gato.draw_gato_full(p)
        elif p.tipo == "lola": lola.draw_gato_full(p)
        elif p.tipo == "mosca": mosca.draw_mosca_full(p)
        elif p.tipo == "KingLi": KingLi.draw_kingli_full(p)
        elif p.tipo == "amongus": amongus.draw_amongus_full(p)
        elif p.tipo == "meteoro": meteoro.draw_metetoro_full(p)
        glPopMatrix()
        
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    
    msg = f"JUGADOR {state.fase_seleccion}: ELIGE A TU HALCON"
    draw_text(250, 550, msg, GLUT_BITMAP_HELVETICA_18, (1, 0.8, 0))
    
    p_actual = state.personajes_pool[state.indice_menu]
    data = stats.get(p_actual.tipo, {"nombre": "???", "vel": 5, "fza": 5, "salto": 5})
    draw_text(50, 150, f"> {data['nombre']} <", GLUT_BITMAP_HELVETICA_18, (0, 1, 1))
    draw_stats_bar(50, 110, "Velocidad:", data["vel"], 10, (0, 0.8, 1))
    draw_stats_bar(50, 80, "Fuerza:", data["fza"], 10, (1, 0.2, 0.2))
    draw_stats_bar(50, 50, "Salto:", data["salto"], 10, (0.2, 1, 0.2)) 
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def _draw_centered_text(x, y, text, color=(1,1,1), font=GLUT_BITMAP_HELVETICA_18):
    text_width = len(text) * 8
    draw_text(x - text_width // 2, y, text, font=font, color=color)

def draw_scenario_menu():
    width = glutGet(GLUT_WINDOW_WIDTH)
    height = glutGet(GLUT_WINDOW_HEIGHT)
    glClearColor(0.05, 0.05, 0.12, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)

    title_text = "ELIGE TU NIVEL" if state.modo_juego == 'niveles' else "ELIGE TU ESCENARIO"
    _draw_centered_text(width * 0.5, height - 80, title_text, color=(1, 0.9, 0.4), font=GLUT_BITMAP_HELVETICA_18)
    draw_text(80, height - 120, f"P1: {state.p1.tipo.upper()}    P2: {state.p2.tipo.upper()}", GLUT_BITMAP_HELVETICA_18, (1, 1, 1))
    draw_text(80, height - 140, "Usa FLECHAS para mover el cursor y ENTER para iniciar", GLUT_BITMAP_HELVETICA_12, (0.8, 0.8, 0.8))

    current_pool = state.niveles_pool if state.modo_juego == 'niveles' else state.escenarios_pool
    num_scenarios = len(current_pool)
    cols = 3
    rows = (num_scenarios + cols - 1) // cols

    margin_x = 50
    margin_y = 150
    spacing_x = 30
    spacing_y = 30
    box_w = (width - margin_x * 2 - spacing_x * (cols - 1)) / cols
    box_h = (height - margin_y * 2 - spacing_y * (rows - 1)) / rows

    positions = []
    for r in range(rows):
        for c in range(cols):
            if len(positions) >= num_scenarios: 
                break
            x0 = margin_x + c * (box_w + spacing_x)
            y0 = height - margin_y - (r + 1) * box_h - r * spacing_y
            x1 = x0 + box_w
            y1 = y0 + box_h
            positions.append((x0, y0, x1, y1))

    for i, option in enumerate(current_pool):
        x0, y0, x1, y1 = positions[i]
        r, g, b = option["color"]
        glColor3f(r * 0.35, g * 0.35, b * 0.35)
        glBegin(GL_QUADS)
        glVertex2f(x0, y0)
        glVertex2f(x1, y0)
        glVertex2f(x1, y1)
        glVertex2f(x0, y1)
        glEnd()

        glColor3f(r, g, b)
        glBegin(GL_QUADS)
        glVertex2f(x0 + 10, y0 + 10)
        glVertex2f(x1 - 10, y0 + 10)
        glVertex2f(x1 - 10, y1 - 10)
        glVertex2f(x0 + 10, y1 - 10)
        glEnd()

        if i == state.indice_escenario:
            glLineWidth(5.0)
            glColor3f(1.0, 1.0, 1.0)
            glBegin(GL_LINE_LOOP)
            glVertex2f(x0 + 4, y0 + 4)
            glVertex2f(x1 - 4, y0 + 4)
            glVertex2f(x1 - 4, y1 - 4)
            glVertex2f(x0 + 4, y1 - 4)
            glEnd()
            glLineWidth(1.0)

        title = option["nombre"]
        _draw_centered_text((x0 + x1) / 2, y1 - box_h * 0.5, title, color=(1, 1, 1))

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_pause_menu():
    width = glutGet(GLUT_WINDOW_WIDTH)
    height = glutGet(GLUT_WINDOW_HEIGHT)
    glClearColor(0.03, 0.03, 0.06, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)

    _draw_centered_text(width * 0.5, height - 90, "PAUSA", color=(1, 0.9, 0.4))
    draw_text(40, height - 140, "Usa las flechas para moverte y ENTER para seleccionar.", GLUT_BITMAP_HELVETICA_12, (0.8, 0.8, 0.8))

    base_y = height - 220
    step = 70
    for index, label in enumerate(state.pause_menu_options):
        y = base_y - index * step
        box_x0 = width * 0.2
        box_x1 = width * 0.8
        box_y0 = y - 30
        box_y1 = y + 20
        if index == state.indice_pausa:
            glColor3f(0.2, 0.5, 0.9)
            glBegin(GL_QUADS)
            glVertex2f(box_x0, box_y0)
            glVertex2f(box_x1, box_y0)
            glVertex2f(box_x1, box_y1)
            glVertex2f(box_x0, box_y1)
            glEnd()
            text_color = (1, 1, 1)
        else:
            glColor3f(0.12, 0.12, 0.18)
            glBegin(GL_QUADS)
            glVertex2f(box_x0, box_y0)
            glVertex2f(box_x1, box_y0)
            glVertex2f(box_x1, box_y1)
            glVertex2f(box_x0, box_y1)
            glEnd()
            text_color = (0.8, 0.8, 0.9)

        _draw_centered_text((box_x0 + box_x1) * 0.5, y - 6, label, color=text_color)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_help_menu():
    width = glutGet(GLUT_WINDOW_WIDTH)
    height = glutGet(GLUT_WINDOW_HEIGHT)
    glClearColor(0.03, 0.03, 0.06, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)

    _draw_centered_text(width * 0.5, height - 90, "AYUDA", color=(1, 0.9, 0.4))
    controls = [
        "CONTROLES JUGADOR 1:",
        "- Mover: W, A, S, D  |  Saltar: F  |  Disparar Balón: E (Nivel 2)",
        "- Trivia: W/S para elegir, A para confirmar",
        "",
        "CONTROLES JUGADOR 2:",
        "- Mover: Flechas  |  Saltar: ESPACIO  |  Disparar Balón: ENTER (Nivel 2)",
        "- Trivia: Flechas Arriba/Abajo para elegir, ENTER para confirmar",
        "",
        "OBJETIVO DEL JUEGO Y COMO NO PERDER:",
        "1. Esquiva los obstaculos (cubos, barreras y esferas) saltando o moviendote.",
        "2. Si chocas, deberas responder una pregunta de trivia.",
        "3. Si respondes mal, pierdes una vida.",
        "4. ¡Gana el ultimo jugador en pie!"
    ]
    y_pos = height - 130
    for line in controls:
        if line == "":
            y_pos -= 10
        elif line.startswith("CONTROLES") or line.startswith("OBJETIVO"):
            draw_text(80, y_pos, line, GLUT_BITMAP_HELVETICA_18, (1, 0.9, 0.4))
            y_pos -= 25
        else:
            draw_text(90, y_pos, line, GLUT_BITMAP_HELVETICA_18, (1, 1, 1))
            y_pos -= 25

    draw_text(80, 80, "Presiona ESC o ENTER para volver al menú de pausa.", GLUT_BITMAP_HELVETICA_12, (0.8, 0.8, 0.8))

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if state.estado_actual == state.MENU_PRINCIPAL:
        glViewport(0, 0, glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
        draw_main_menu()
    elif state.estado_actual == state.MENU_SELECCION:
        glViewport(0, 0, glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
        draw_multijugador_menu() 
    elif state.estado_actual == state.MENU_ESCENARIO:
        glViewport(0, 0, glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
        draw_scenario_menu()
    elif state.estado_actual == state.MENU_PAUSA:
        glViewport(0, 0, glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
        draw_pause_menu()
    elif state.estado_actual == state.MENU_AYUDA:
        glViewport(0, 0, glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
        draw_help_menu()
    elif state.estado_actual == state.EN_JUEGO:
        width = glutGet(GLUT_WINDOW_WIDTH)
        height = glutGet(GLUT_WINDOW_HEIGHT)
        half_width = width // 2
        # vista jugador 1
        glViewport(0, 0, half_width, height)
        render_player_view(state.p1, half_width, height)
        draw_player_status(state.p1, 20, 560)
        draw_text_2d(20, 20, "P1", (0, 1, 1))
        # jugador 2
        glViewport(half_width, 0, half_width, height)
        render_player_view(state.p2, half_width, height)
        draw_player_status(state.p2, 20, 560)
        draw_text_2d(20, 20, "P2", (1, 0.5, 0))
        
        draw_level1_overlay(width, height)
        draw_level2_overlay(width, height) # Nueva interfaz del Nivel de Balones
     
    glutSwapBuffers()

def render_player_view(player_to_follow, view_w, view_h):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, view_w / view_h, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    camera.apply_camera_to_player(player_to_follow)
    luz.apply_light_position()
    luz.apply_shading()
    
    grid.draw_grid(size=30, step=1)
    grid.draw_axes()
    escenario.draw_scenery(state.scenario)
    
    if state.level1_enabled and state.level1_phase == state.LEVEL1_ACTIVE:
        for hazard in state.level1_hazards:
            hazard.draw()


    if getattr(state, 'level_balones_enabled', False):
        for balon in getattr(state, 'level_balones_jugador', []):
            glPushMatrix()
            glTranslatef(balon['x'], balon['y'], balon['z'])
            glColor3f(*balon['color'])
            # Renderizamos una esfera sólida como balón usando su atributo 'size'
            glutSolidSphere(balon['size'], 16, 16)
            glPopMatrix()

    # Dibujar Sombras de ambos jugadores
    state.is_shadow_pass = True
    glDisable(GL_LIGHTING)
    glPushMatrix()
    shadow_mat = luz.get_shadow_matrix()
    glMultMatrixf(shadow_mat)
    draw_players() 
    glPopMatrix()
    glEnable(GL_LIGHTING)
    state.is_shadow_pass = False
    
    # dibujar jugadores normalmente
    draw_players()

def draw_text_2d(x, y, text, color):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    draw_text(x, y, text, GLUT_BITMAP_HELVETICA_18, color)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_player_status(player, x, y):
    label = f"{player.nombre} - Vidas: {player.lives}"
    draw_text_2d(x, y, label, (1, 1, 1))

def draw_level1_overlay(width, height):
    if not state.level1_enabled:
        return
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    if state.level1_phase == state.LEVEL1_WAITING:
        draw_text(150, 540, "Sala de espera: coloquense en las dos plataformas", GLUT_BITMAP_HELVETICA_12, (1, 1, 0))
        draw_text(200, 520, "P1 en plataforma izq. - P2 en plataforma der.", GLUT_BITMAP_HELVETICA_12, (1, 1, 0))
    elif state.level1_phase == state.LEVEL1_TRANSITION:
        glColor4f(0, 0, 0, state.level1_transition_alpha)
        glBegin(GL_QUADS)
        glVertex2f(0, 0); glVertex2f(800, 0)
        glVertex2f(800, 600); glVertex2f(0, 600)
        glEnd()
        draw_stroke_text(200, 330, state.level1_message, scale=0.4, color=(1, 1, 1), line_width=2.0)
    elif state.level1_phase == state.LEVEL1_COUNTDOWN:
        glColor4f(0, 0, 0, 0.85)
        glBegin(GL_QUADS)
        glVertex2f(0, 0); glVertex2f(800, 0)
        glVertex2f(800, 600); glVertex2f(0, 600)
        glEnd()
        draw_stroke_text(320, 320, str(max(state.level1_countdown, 1)), scale=0.8, color=(1, 1, 1), line_width=5.0)
        draw_text(300, 260, "Cuenta regresiva...", GLUT_BITMAP_HELVETICA_18, (1, 1, 1))
    elif state.level1_phase == state.LEVEL1_TRIVIA:
        if state.level1_question_target == 'p1':
            glColor4f(0, 0, 0, 0.85)
            glBegin(GL_QUADS)
            glVertex2f(0, 0); glVertex2f(400, 0)
            glVertex2f(400, 600); glVertex2f(0, 600)
            glEnd()
            y_start = 550
            draw_text(20, y_start, "TRIVIA", GLUT_BITMAP_HELVETICA_18, (1, 1, 0))
            if state.level1_current_question:
                pregunta = state.level1_current_question["pregunta"]
                if len(pregunta) > 40:
                    pregunta_lines = [pregunta[i:i+40] for i in range(0, len(pregunta), 40)]
                    y_start -= 30
                    for line in pregunta_lines:
                        draw_text(20, y_start, line, GLUT_BITMAP_HELVETICA_12, (1, 1, 1))
                        y_start -= 20
                else:
                    draw_text(20, y_start - 30, pregunta, GLUT_BITMAP_HELVETICA_12, (1, 1, 1))
                    y_start -= 60
                opciones = state.level1_current_question["opciones"]
                opt_y = y_start
                for i, opcion in enumerate(opciones):
                    color = (1, 1, 0) if i == state.level1_selected_option else (0.7, 0.7, 0.7)
                    if i == state.level1_selected_option:
                        glColor3f(0.2, 0.5, 0.2)
                        glBegin(GL_QUADS)
                        glVertex2f(15, opt_y - 5); glVertex2f(385, opt_y - 5)
                        glVertex2f(385, opt_y + 15); glVertex2f(15, opt_y + 15)
                        glEnd()
                    draw_text(25, opt_y, f"{chr(65+i)}) {opcion}", GLUT_BITMAP_HELVETICA_12, color)
                    opt_y -= 30
                if state.level1_show_feedback_msg:
                    draw_text(20, 80, state.level1_feedback_msg, GLUT_BITMAP_HELVETICA_12, (1, 1, 0))
        elif state.level1_question_target == 'p2':
            glColor4f(0, 0, 0, 0.85)
            glBegin(GL_QUADS)
            glVertex2f(400, 0); glVertex2f(800, 0)
            glVertex2f(800, 600); glVertex2f(400, 600)
            glEnd()
            y_start = 550
            draw_text(420, y_start, "TRIVIA", GLUT_BITMAP_HELVETICA_18, (1, 1, 0))
            if state.level1_current_question:
                pregunta = state.level1_current_question["pregunta"]
                if len(pregunta) > 40:
                    pregunta_lines = [pregunta[i:i+40] for i in range(0, len(pregunta), 40)]
                    y_start -= 30
                    for line in pregunta_lines:
                        draw_text(420, y_start, line, GLUT_BITMAP_HELVETICA_12, (1, 1, 1))
                        y_start -= 20
                else:
                    draw_text(420, y_start - 30, pregunta, GLUT_BITMAP_HELVETICA_12, (1, 1, 1))
                    y_start -= 60
                opciones = state.level1_current_question["opciones"]
                opt_y = y_start
                for i, opcion in enumerate(opciones):
                    color = (1, 1, 0) if i == state.level1_selected_option else (0.7, 0.7, 0.7)
                    if i == state.level1_selected_option:
                        glColor3f(0.2, 0.5, 0.2)
                        glBegin(GL_QUADS)
                        glVertex2f(415, opt_y - 5); glVertex2f(785, opt_y - 5)
                        glVertex2f(785, opt_y + 15); glVertex2f(415, opt_y + 15)
                        glEnd()
                    draw_text(425, opt_y, f"{chr(65+i)}) {opcion}", GLUT_BITMAP_HELVETICA_12, color)
                    opt_y -= 30
                if state.level1_show_feedback_msg:
                    draw_text(420, 80, state.level1_feedback_msg, GLUT_BITMAP_HELVETICA_12, (1, 1, 0))
    elif state.level1_phase == state.LEVEL1_FINISHED:
        glColor4f(0, 0, 0, 1.0)
        glBegin(GL_QUADS)
        glVertex2f(0, 0); glVertex2f(800, 0)
        glVertex2f(800, 600); glVertex2f(0, 600)
        glEnd()
        winner_name = state.p1.nombre if state.level1_winner == 'p1' else state.p2.nombre
        draw_stroke_text(150, 400, f"GANA: {winner_name}", scale=0.5, color=(1, 1, 0), line_width=4.0)
        draw_text(250, 300, "Presione una opcion:", GLUT_BITMAP_HELVETICA_18, (1, 1, 1))
        draw_text(260, 260, "R - Repetir Nivel", GLUT_BITMAP_HELVETICA_18, (0.7, 1, 0.7))
        draw_text(260, 230, "S - Seleccionar Nivel", GLUT_BITMAP_HELVETICA_18, (0.7, 1, 0.7))
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_level2_overlay(width, height):
    if state.scenario != 5 or not hasattr(state, 'level2_phase') or state.level2_phase == state.LEVEL2_NONE:
        return

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)


    if not getattr(state, 'level2_game_over', False):
        # Alineación hacia la esquina superior izquierda (X = 20)
        draw_text(20, 530, "¡BATALLA DE BALONES EN EL NIDO!", GLUT_BITMAP_HELVETICA_12, (0.0, 0.9, 1.0))
        draw_text(20, 510, "Objetivo: Resta vidas al rival disparando balones.", GLUT_BITMAP_HELVETICA_10, (1, 1, 1))
        draw_text(20, 490, "P1 Controles: WASD | E para Disparar", GLUT_BITMAP_HELVETICA_10, (0.4, 1.0, 0.4))
        draw_text(20, 470, "P2 Controles: Flechas | ENTER para Disparar", GLUT_BITMAP_HELVETICA_10, (1.0, 0.6, 0.0))

        if state.level2_phase == state.LEVEL2_WAITING:
            draw_text(150, 320, "Sala de espera: coloquense listos para la batalla", GLUT_BITMAP_HELVETICA_18, (1, 1, 0))
            draw_text(220, 290, "Presionen sus botones de disparo para iniciar", GLUT_BITMAP_HELVETICA_12, (1, 1, 1))
            
        elif state.level2_phase == state.LEVEL2_TRANSITION:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glColor4f(0, 0, 0, getattr(state, 'level2_transition_alpha', 0.7))
            glBegin(GL_QUADS)
            glVertex2f(0, 0); glVertex2f(800, 0)
            glVertex2f(800, 600); glVertex2f(0, 600)
            glEnd()
            glDisable(GL_BLEND)
            
            msg_nivel = getattr(state, 'level2_message', "CARGANDO NIVEL 2...")
            draw_stroke_text(200, 300, msg_nivel, scale=0.4, color=(1, 1, 1), line_width=2.0)
            
        elif state.level2_phase == state.LEVEL2_COUNTDOWN:
            glColor4f(0, 0, 0, 0.6)
            glBegin(GL_QUADS)
            glVertex2f(0, 0); glVertex2f(800, 0)
            glVertex2f(800, 600); glVertex2f(0, 600)
            glEnd()
            
            cuenta = str(max(getattr(state, 'level2_countdown', 3), 1))
            draw_stroke_text(370, 300, cuenta, scale=0.8, color=(1, 1, 0), line_width=5.0)

    else:
        # Fondo oscuro completo
        glColor4f(0.0, 0.0, 0.0, 1.0)
        glBegin(GL_QUADS)
        glVertex2f(0, 0); glVertex2f(800, 0)
        glVertex2f(800, 600); glVertex2f(0, 600)
        glEnd()
        

        ganador_id = getattr(state, 'level2_winner', None)
        nombre_ganador = "EMPATE"
        if ganador_id == 'p1':
            nombre_ganador = state.p1.nombre
        elif ganador_id == 'p2':
            nombre_ganador = state.p2.nombre
            

        draw_stroke_text(150, 400, f"GANA : {nombre_ganador}", scale=0.5, color=(0.0, 0.9, 1.0), line_width=4.0)
        
  
        draw_text(250, 300, "Presione una opcion:", GLUT_BITMAP_HELVETICA_18, (1, 1, 1))
        draw_text(260, 260, "R - Repetir Nivel", GLUT_BITMAP_HELVETICA_18, (0.7, 1, 0.7))
        draw_text(260, 230, "S - Seleccionar Nivel", GLUT_BITMAP_HELVETICA_18, (1.0, 0.6, 0.0))

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def reshape(w, h):
    if h == 0: h = 1
    glViewport(0, 0, w, h)


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(900, 700)
    gestor_audio.play_background_music(1)
    glutCreateWindow(b"Timoteo 3D - Menu System")
    init()
    
    # Vinculación de Callbacks de Dibujo y Ventana
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    
    # Vinculación de Callbacks desde input_handlers
    glutKeyboardFunc(input_handlers.keyboard)
    glutSpecialFunc(input_handlers.special_keys)
    glutMouseFunc(input_handlers.mouse)
    glutMotionFunc(input_handlers.motion)
    
    # Sistema de tiempo de actualización física y lógica
    glutTimerFunc(16, update.update, 0)
    
    # Vinculación de Callbacks al soltar teclas
    glutKeyboardUpFunc(input_handlers.keyboard_up)
    glutSpecialUpFunc(input_handlers.keyboard_special_up)
    
    glutMainLoop()

if __name__ == "__main__":
    main()