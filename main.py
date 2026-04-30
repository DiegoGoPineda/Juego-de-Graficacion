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
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    """   
    # Cámara Fija
    gluLookAt(
        0,1.5,6, #Posicion de la camara
        0,0,0,  # Punto al que mira
        0,1,0  # Vector altura al que se coloca
    )
    """
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
    """
    #dibuja a a lola
    glPushMatrix()
    glTranslatef(state.p2.x, state.p2.y, state.p2.z)
    lola.draw_gato_full(state.p2) # Dibuja la lola completa jugador 2
    """
    #dibujar la mosca
    glPushMatrix()
    glTranslatef(state.p2.x, state.p2.y, state.p2.z)
    mosca.draw_mosca_full(state.p2) # Dibuja la mosca completa jugador 2
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