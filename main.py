from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from resources import escenario
from Actions import state, camera, update, gestor_audio, luz
from Characteres import gato, lola, mosca, KingLi
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
    # Tipografía vectorial profesional para títulos
    glDisable(GL_LIGHTING)
    glColor3f(*color)
    glLineWidth(line_width)
    glPushMatrix()
    glTranslatef(x, y, 0)
    glScalef(scale, scale, 1.0) # Escalamos la fuente gigante
    for char in text:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))
    glPopMatrix()
    glLineWidth(1.0) # Restauramos el grosor normal
    glEnable(GL_LIGHTING)
def draw_stats_bar(x, y, label, value, max_value=10, color=(0, 1, 0)):
    """
    Dibuja una barra de estadísticas con estética profesional, 
    degradados y brillo tipo cristal.
    """
    # 1. Dibujar la etiqueta con un ligero desplazamiento para mejor legibilidad
    # Usamos blanco puro para el texto
    draw_text(x, y + 4, label, GLUT_BITMAP_HELVETICA_12, (1, 1, 1))

    # --- PREPARACIÓN DE UI ---
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND) # Habilitamos blending para el brillo translúcido
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Configuración de dimensiones
    offset_x = 100  # Espacio para el texto
    ancho_total = 200
    alto = 12
    ancho_relleno = ancho_total * (value / max_value)

    # 2. Dibujar el FONDO (Gris muy oscuro con profundidad)
    glBegin(GL_QUADS)
    glColor4f(0.05, 0.05, 0.05, 0.8) # Casi negro
    glVertex2f(x + offset_x, y)
    glVertex2f(x + offset_x + ancho_total, y)
    glColor4f(0.15, 0.15, 0.15, 0.8) # Un poco más claro arriba
    glVertex2f(x + offset_x + ancho_total, y + alto)
    glVertex2f(x + offset_x, y + alto)
    glEnd()

    # 3. Dibujar el RELLENO con DEGRADADO (Gouraud Shading)
    # Esto le da un aspecto metálico/tecnológico
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

    # 4. CAPA DE BRILLO (Efecto Cristal)
    # Dibujamos un brillo blanco translúcido en la mitad superior de la barra
    glBegin(GL_QUADS)
    glColor4f(1.0, 1.0, 1.0, 0.2) # Blanco muy suave
    glVertex2f(x + offset_x, y + (alto / 2))
    glVertex2f(x + offset_x + ancho_relleno, y + (alto / 2))
    glColor4f(1.0, 1.0, 1.0, 0.0) # Desvanece a transparente
    glVertex2f(x + offset_x + ancho_relleno, y + alto)
    glVertex2f(x + offset_x, y + alto)
    glEnd()

    # 5. BORDE (Outline sutil)
    glLineWidth(1.0)
    glBegin(GL_LINE_LOOP)
    glColor4f(1.0, 1.0, 1.0, 0.3) # Borde blanco tenue
    glVertex2f(x + offset_x, y)
    glVertex2f(x + offset_x + ancho_total, y)
    glVertex2f(x + offset_x + ancho_total, y + alto)
    glVertex2f(x + offset_x, y + alto)
    glEnd()

    # --- RESTAURAR ESTADOS ---
    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

def draw_players():
    # Dibujamos a los jugadores según su tipo (Gato, Lola, Mosca o KingLi)
    # Jugador 1
    glPushMatrix()
    glTranslatef(state.p1.x, state.p1.y, state.p1.z)
    if state.p1.tipo == "gato": gato.draw_gato_full(state.p1)
    elif state.p1.tipo == "mosca": mosca.draw_mosca_full(state.p1)
    elif state.p1.tipo == "lola": lola.draw_gato_full(state.p1)
    elif state.p1.tipo == "KingLi": KingLi.draw_kingli_full(state.p1)
    glPopMatrix()

    # Jugador 2
    glPushMatrix()
    glTranslatef(state.p2.x, state.p2.y, state.p2.z)
    if state.p2.tipo == "gato": gato.draw_gato_full(state.p2)
    elif state.p2.tipo == "mosca": mosca.draw_mosca_full(state.p2)
    elif state.p2.tipo == "lola": lola.draw_gato_full(state.p2)
    elif state.p2.tipo == "KingLi": KingLi.draw_kingli_full(state.p2)
    glPopMatrix()
def draw_ittol_logo(x, y, radius, angle=0.0):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glRotatef(angle, 0, 0, 1)
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    
    # 1. Dientes del engrane azul (Rotación matricial)
    glColor3f(0.0, 0.2, 0.6) # Azul Tec
    for i in range(12):
        glPushMatrix()
        glRotatef(i * 30, 0, 0, 1) # 12 dientes = 360/12 grados
        glBegin(GL_QUADS)
        glVertex2f(-radius * 0.15, radius * 0.8)
        glVertex2f(radius * 0.15, radius * 0.8)
        glVertex2f(radius * 0.1, radius * 1.15)
        glVertex2f(-radius * 0.1, radius * 1.15)
        glEnd()
        glPopMatrix()
    
    # 2. Base del engrane (Círculo azul)
    glBegin(GL_POLYGON)
    for i in range(36):
        theta = 2.0 * math.pi * i / 36
        glVertex2f(radius * math.cos(theta), radius * math.sin(theta))
    glEnd()

    # 3. Centro verde (Simulando el campo/cerro)
    glColor3f(0.0, 0.7, 0.3)
    glBegin(GL_POLYGON)
    for i in range(36):
        theta = 2.0 * math.pi * i / 36
        glVertex2f(radius * 0.65 * math.cos(theta), radius * 0.65 * math.sin(theta))
    glEnd()
    
    # 4. Hueco central (Fondo oscuro para darle forma de aro)
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
    
    # Colores retro arcade: Rosa neón, Cyan y Amarillo
    colores = [(1.0, 0.2, 0.6), (0.0, 0.8, 1.0), (1.0, 0.9, 0.0)]
    
    start_x = 120  # Dónde empiezan
    espaciado = 40 # Distancia entre estrellas
    
    for i in range(15):
        x = start_x + (i * espaciado)
        # Magia matemática: Cambia el índice del color basado en la posición y el tiempo
        color_idx = int((tiempo_ms / 150) + i) % 3 
        glColor3f(*colores[color_idx])
        
        # Dibujamos un "píxel" rotado 45 grados (un rombo) para simular la estrella
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
    # Fondo azul muy oscuro
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

    # ==========================================
    # 1. ELEMENTOS DE IDENTIDAD ITTOL
    # ==========================================
    # Barra superior naranja
    glColor3f(1.0, 0.4, 0.0) 
    glBegin(GL_QUADS)
    glVertex2f(0, 580); glVertex2f(800, 580)
    glVertex2f(800, 600); glVertex2f(0, 600)
    glEnd()
    
    # Líneas tecnológicas azules (Ajustadas más abajo)
    glLineWidth(3.0)
    glColor3f(0.0, 0.4, 0.8) 
    glBegin(GL_LINES)
    glVertex2f(0, 475); glVertex2f(800, 475)
    glVertex2f(0, 465); glVertex2f(800, 465)
    glEnd()

    tiempo_actual = glutGet(GLUT_ELAPSED_TIME)

    # --- Logo del Tec GIRATORIO ---
    # Lo bajamos a Y=280 para que no choque con el texto superior
    draw_ittol_logo(400, 280, 120, angle=tiempo_actual * 0.02)
    
    # FIX: El logo reactiva la profundidad, la apagamos de nuevo para salvar el texto de los botones
    glDisable(GL_DEPTH_TEST)

    # ==========================================
    # 2. TIPOGRAFÍA PRO Y MARQUESINA
    # ==========================================
    # Estrellas arriba del título
    draw_arcade_stars(560, tiempo_actual)
    # Estrellas hasta abajo de la pantalla (Footer arcade)
    draw_arcade_stars(60, tiempo_actual)

    # Título Principal (Ajustado en Y=490)
    texto_titulo = "CONOCE-TEC"
    draw_stroke_text(165, 490, texto_titulo, scale=0.5, color=(1, 1, 1), line_width=4.0)

    # Eslogan nuevo (Ajustado en Y=425)
    texto_sub = "CONOCE EL NIDO"
    draw_stroke_text(265, 425, texto_sub, scale=0.2, color=(1.0, 0.6, 0.0), line_width=2.5)

    # ==========================================
    # 3. INTERFAZ DE BOTONES MEJORADA
    # ==========================================
    opciones = ["JUGAR", "SALIR"]
    for i, texto in enumerate(opciones):
        # Separamos más los botones (Jugar=250, Salir=130)
        y_base = 250 - (i * 120) 
        glDisable(GL_LIGHTING)
        
        if i == state.indice_boton:
            # BOTÓN SELECCIONADO
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
            
            # Punteros
            glBegin(GL_TRIANGLES)
            glVertex2f(230, y_base + 25); glVertex2f(260, y_base + 40); glVertex2f(260, y_base + 10)
            glVertex2f(570, y_base + 25); glVertex2f(540, y_base + 40); glVertex2f(540, y_base + 10)
            glEnd()
            
            color_texto = (1, 1, 1) 
        else:
            # BOTÓN INACTIVO
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
    #intrucciones
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
    # 1. Limpieza de buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # 2. Diccionario de datos (Para evitar el NameError de 'stats')
    stats = {
        "gato": {"nombre": "Timoteo", "vel": 9, "fza": 3, "salto": 8},
        "lola": {"nombre": "Lola", "vel": 4, "fza": 3, "salto": 5},
        "mosca": {"nombre": "Cartonix", "vel": 6, "fza": 6, "salto": 6},
        "KingLi": {"nombre": "King-Lee", "vel": 8, "fza": 8, "salto": 8}
    }

    # ==========================================
    # CAPA 3D: PERSONAJES (Efecto HD Vibrante)
    # ==========================================
    glLoadIdentity()
    
    # Cámara dinámica
    cam_x = (state.indice_menu - 2.5) * 5.5
    gluLookAt(cam_x, 2, 16, cam_x, 0, 0, 0, 1, 0)
    
    # --- CONFIGURACIÓN DE LUZ MAESTRA ---
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    # TRUCO: Luz ambiental casi al máximo para que nada se vea oscuro u opaco
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.7, 0.7, 0.7, 1.0]) 
    
    # Reforzamos la posición de la luz para que cree los bordes HD
    luz.apply_light_position() 

    for i, p in enumerate(state.personajes_pool):
        glPushMatrix()
        x_pos = (i - 2.5) * 5.5 
        glTranslatef(x_pos, -2.0, 0)

        # Reset de color a blanco puro para no heredar colores de las barras
        glColor3f(1.0, 1.0, 1.0) 

        if i == state.indice_menu:
            # SELECCIONADO: Grande, brillante y con rotación
            glScalef(1.5, 1.5, 1.5) 
            glRotatef(glutGet(GLUT_ELAPSED_TIME) * 0.05, 0, 1, 0) 
            
            # Le damos un "auto-brillo" sutil para que no se vea opaco
            glMaterialfv(GL_FRONT, GL_EMISSION, [0.2, 0.2, 0.2, 1.0])
            glMaterialf(GL_FRONT, GL_SHININESS, 80.0)
        else:
            # NO SELECCIONADOS: Un poco más oscuros pero con volumen visible
            glScalef(0.8, 0.8, 0.8)
            glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])
            glColor3f(0.5, 0.5, 0.5) 

        # Renderizado de modelos
        if p.tipo == "gato": gato.draw_gato_full(p)
        elif p.tipo == "lola": lola.draw_gato_full(p)
        elif p.tipo == "mosca": mosca.draw_mosca_full(p)
        elif p.tipo == "KingLi": KingLi.draw_kingli_full(p)

        glPopMatrix()

    # ==========================================
    # CAPA 2D: HUD (Barras Pro y Texto)
    # ==========================================
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Desactivamos iluminación para la interfaz
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)

    # Título y Nombres
    msg = f"JUGADOR {state.fase_seleccion}: ELIGE A TU HALCON"
    draw_text(250, 550, msg, GLUT_BITMAP_HELVETICA_18, (1, 0.8, 0))
    
    p_actual = state.personajes_pool[state.indice_menu]
    data = stats.get(p_actual.tipo, {"nombre": "Halcón", "vel": 5, "fza": 5, "salto": 5})
    
    # Nombre y barras con el diseño "lindísimo"
    draw_text(50, 150, f"> {data['nombre']} <", GLUT_BITMAP_HELVETICA_18, (0, 1, 1))
    draw_stats_bar(50, 110, "Velocidad:", data["vel"], 10, (0, 0.8, 1))
    draw_stats_bar(50, 80, "Fuerza:", data["fza"], 10, (1, 0.2, 0.2))
    draw_stats_bar(50, 50, "Salto:", data["salto"], 10, (0.2, 1, 0.2))
    
    # Restaurar estados para el siguiente frame
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # MÁQUINA DE ESTADOS
    if state.estado_actual == state.MENU_PRINCIPAL:
        draw_main_menu()
    
    elif state.estado_actual == state.MENU_SELECCION:
        draw_multijugador_menu()
    
    elif state.estado_actual == state.EN_JUEGO:
        camera.apply_camera()
        # aplicamos la luz antes de dibujar el escenario y los personajes
        luz.apply_light_position()
        luz.apply_shading()
        # escenario
        grid.draw_grid(size=30, step=1)
        grid.draw_axes()
        escenario.draw_scenery(state.scenario)
        # sombras 
        state.is_shadow_pass = True
        glDisable(GL_LIGHTING)
        glPushMatrix()
        # aplasta el modelo
        shadow_mat = luz.get_shadow_matrix()
        glMultMatrixf(shadow_mat)
        draw_players() 
        glPopMatrix()
        glEnable(GL_LIGHTING)
        state.is_shadow_pass = False
        # personajes con iluminacion
        draw_players()
        if state.show_instructions:
            show_game_instructions()
        
    glutSwapBuffers()

def reshape(w, h):
    if h == 0: h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w/h, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(900, 700)
    gestor_audio.play_background_music(1)
    glutCreateWindow(b"Timoteo 3D - Menu System")
    init()   
    glutDisplayFunc(display)
    glutReshapeFunc(reshape) 
    glutKeyboardFunc(input_handlers.keyboard)     
    glutSpecialFunc(input_handlers.special_keys)     
    glutMouseFunc(input_handlers.mouse)
    glutMotionFunc(input_handlers.motion)
    glutTimerFunc(16, update.update, 0)
    glutKeyboardUpFunc(input_handlers.keyboard_up)
    glutSpecialUpFunc(input_handlers.keyboard_special_up)
    
    glutMainLoop()

if __name__ == "__main__":
    main()
    