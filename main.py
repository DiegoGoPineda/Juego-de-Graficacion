from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from resources import escenario
from Actions import state, camera, update,gestor_audio
from Characteres import gato,lola,mosca
from resources import input_handlers, grid

show_instructions = True
def init():
    glEnable(GL_DEPTH_TEST) 
    glEnable(GL_LIGHTING) 
    glEnable(GL_LIGHT0)      
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    glLightfv(GL_LIGHT0, GL_POSITION, [2.0, 5.0, 5.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glClearColor(0.9, 0.9, 0.9, 1.0)

def draw_text(x, y, text):
    glDisable(GL_LIGHTING)
    glColor3f(0.0, 0.0, 0.0) # Negro
    glRasterPos2f(x, y)
    # Uso de fuente
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(char))
    glEnable(GL_LIGHTING)

def show_menu():
    glDisable(GL_DEPTH_TEST) 
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    instructions = [
        "--- CONTROLES MULTIJUGADOR ---",
        "TIMOTEO (P1): WASD para mover",
        "   Acciones: Q (Cola), E (Ojos), R (Salto), F (Saludar)",
        "LOLA (P2): FLECHAS para mover",
        "   Acciones: Automaticas por colision",
        "-------------------------------",
        "1-7: Cambiar Escenario (Ambos)",
        "0: Mostrar/Ocultar Menu",
        "O: Activar/Desactivar audio",
        "Z-M: Controles de Camara",
        "ESC: Salir"
    ]
    y_pos = 570
    for line in instructions:
        draw_text(20, y_pos, line)
        y_pos -= 20
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    
#Renderizado 
"""
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # aplicar camra 
    camera.apply_camera()
    #ver gril
    grid.draw_grid(size=30, step=1)
    grid.draw_axes()
    #dibujar escenario 
    escenario.draw_scenery(state.scenario)
    #Dibujar gato
    glPushMatrix()
    glTranslatef(state.p1.x, state.p1.y, state.p1.z)
    gato.draw_gato_full(state.p1) # Dibuja el gato completo jugador 1
    glPopMatrix()   
    #dibuja a a lola
    glPushMatrix()
    glTranslatef(state.p2.x, state.p2.y, state.p2.z)
    lola.draw_gato_full(state.p2) # Dibuja la lola completa jugador 2  
    #dibujar la mosca
    glPushMatrix()
    glTranslatef(state.p2.x, state.p2.y, state.p2.z)
    mosca.draw_mosca_full(state.p2) # Dibuja la mosca completa jugador 2
    glPopMatrix()
    if state.show_instructions:
        show_menu()
        
    glutSwapBuffers()
"""
def draw_multijugador_menu():
    glClearColor(0.05, 0.05, 0.1, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # --- DIBUJAR TÍTULO EN 2D ---
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glDisable(GL_LIGHTING)
    glColor3f(1.0, 1.0, 1.0) # Texto blanco para que resalte
    titulo = "JUGADOR 1: ELIGE TU PERSONAJE" if state.fase_seleccion == 1 else "JUGADOR 2: ELIGE TU PERSONAJE"
    # Centrar el texto un poco (x=250, y=550)
    glRasterPos2f(250, 550)
    for char in titulo:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    glEnable(GL_LIGHTING)
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    # ----------------------------

    # Volver a cámara 3D para los personajes
    gluLookAt(0, 0, 15, 0, 0, 0, 0, 1, 0)

    for i, p in enumerate(state.personajes_pool):
        glPushMatrix()
        # Ajustamos el espaciado para que quepan los 3 (Lola, Timoteo, Mosca)
        x_pos = (i - 1) * 7.0 
        glTranslatef(x_pos, -2.0, 0)
        
        glRotatef(glutGet(GLUT_ELAPSED_TIME) * 0.08, 0, 1, 0)

        if i == state.indice_menu:
            glScalef(1.4, 1.4, 1.4)
            tag = "P1" if state.fase_seleccion == 1 else "P2"
            # Dibujar etiqueta sobre el personaje
            draw_text(-0.5, 4, tag)
        else:
            glScalef(0.8, 0.8, 0.8)
            glColor3f(0.3, 0.3, 0.3)

        # Dibujar el personaje según su tipo
        if p.tipo == "gato": 
            gato.draw_gato_full(p)
        elif p.tipo == "lola": 
            lola.draw_gato_full(p)
        elif p.tipo == "mosca": 
            mosca.draw_mosca_full(p)
        
        glPopMatrix()
# nuevo display para el menú multijugador
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    if state.en_menu_seleccion:
        draw_multijugador_menu()
    else:
        camera.apply_camera()
        grid.draw_grid(size=30, step=1)
        grid.draw_axes()
        escenario.draw_scenery(state.scenario)

        # JUGADOR 1
        glPushMatrix()
        glTranslatef(state.p1.x, state.p1.y, state.p1.z)
        if state.p1.tipo == "gato": 
            gato.draw_gato_full(state.p1)
        elif state.p1.tipo == "mosca": 
            mosca.draw_mosca_full(state.p1)
        elif state.p1.tipo == "lola": 
            lola.draw_gato_full(state.p1)
        glPopMatrix()

        # JUGADOR 2
        glPushMatrix()
        glTranslatef(state.p2.x, state.p2.y, state.p2.z)
        if state.p2.tipo == "gato": 
            gato.draw_gato_full(state.p2)
        elif state.p2.tipo == "mosca": 
            mosca.draw_mosca_full(state.p2)
        elif state.p2.tipo == "lola":  
            lola.draw_gato_full(state.p2)
        glPopMatrix()

        if state.show_instructions:
            show_menu()
        
    glutSwapBuffers()
def reshape(w, h):
    if h==0:
        h=1
    global width, height
    width, height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w/h, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    gestor_audio.play_background_music(1)
    glutCreateWindow(b"Timooteoen3D-OpenGL")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape) 
    # 1. Letras y Números (W, A,S, D, T, 1, 2, 3...)
    glutKeyboardFunc(input_handlers.keyboard)    
    # 2. Flechas (Cámara)
    glutSpecialFunc(input_handlers.special_keys)    
    # 3. Mouse y Timer
    glutMouseFunc(input_handlers.mouse)
    glutMotionFunc(input_handlers.motion)
    glutTimerFunc(16, update.update, 0)
    glutKeyboardUpFunc(input_handlers.keyboard_up)
    glutSpecialUpFunc(input_handlers.keyboard_special_up)
    glutMainLoop()
   
if __name__ == "__main__":
    main()

