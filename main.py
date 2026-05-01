from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from resources import escenario
from Actions import state, camera, update, gestor_audio, luz
from Characteres import gato, lola, mosca, KingLi
from resources import input_handlers, grid

def init():
    glEnable(GL_DEPTH_TEST) 
    glEnable(GL_LIGHTING) 
    glEnable(GL_LIGHT0)      
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
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

def draw_main_menu():
    # boton para jugar y salir
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Título Principal
    draw_text(260, 500, "ConeceTec el peak", GLUT_BITMAP_HELVETICA_18, (1, 0.8, 0))

    # Botones
    opciones = ["JUGAR", "SALIR"]
    for i, texto in enumerate(opciones):
        y_pos = 300 - (i * 80)
        # Resaltado si el índice coincide
        color = (0, 1, 0.2) if i == state.indice_boton else (0.6, 0.6, 0.6)
        txt = f"> {texto} <" if i == state.indice_boton else texto
        draw_text(350, y_pos, txt, GLUT_BITMAP_HELVETICA_18, color)

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
    # escoger personajes
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Título de selección
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    msg = f"JUGADOR {state.fase_seleccion}: ELIGE TU PERSONAJE"
    draw_text(220, 550, msg, GLUT_BITMAP_HELVETICA_18, (1,1,1))
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    gluLookAt(0, 0, 18, 0, 0, 0, 0, 1, 0)
    luz.apply_light_position()

    for i, p in enumerate(state.personajes_pool):
        glPushMatrix()
        # Distribución de los 6 personajes en el menú
        x_pos = (i - 2.5) * 5.5 
        glTranslatef(x_pos, -2.0, 0)
        glRotatef(glutGet(GLUT_ELAPSED_TIME) * 0.08, 0, 1, 0)

        if i == state.indice_menu:
            glScalef(1.3, 1.3, 1.3)
            tag = "P1" if state.fase_seleccion == 1 else "P2"
            draw_text(-0.5, 5, tag, color=(1, 1, 0))
        else:
            glScalef(0.7, 0.7, 0.7)
            glColor3f(0.3, 0.3, 0.3)

        if p.tipo == "gato": gato.draw_gato_full(p)
        elif p.tipo == "lola": lola.draw_gato_full(p)
        elif p.tipo == "mosca": mosca.draw_mosca_full(p)
        elif p.tipo == "KingLi": KingLi.draw_kingli_full(p)
        glPopMatrix()

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
    