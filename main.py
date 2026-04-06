from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from resources import escenario
from Actions import state, camera, update,gestor_audio
from Characteres import gato
from resources import input_handlers, grid

show_instructions = True
def init():
    glEnable(GL_DEPTH_TEST) 
    glDisable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glLightfv(GL_LIGHT0, GL_POSITION, [2.0,5.0,5.0,1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2,0.2,0.2,1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8,0.8,0.8,1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0,1.0,1.0,1.0])
    glClearColor(252.0, 252.0, 252.0, 1.0)

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
        "--- CONTROL DE Timoteo ---",
        "0: Ocultar/Mostrar Menu",
        "1-7: neutral, feliz, triste, ira, sorpresa",
        "6, 7: Miedo (Sacudir), Interes",
        "W: Saltar, A: Girar, S: Caminar",
        "D: Cola, I: Parpadeo, J: Patas Arriba",
        "K: Saludar, L: Mover Orejas",
        "FLECHAS: Mover",
        "O Activar/Desactivar audio",
        "Z-M: Movimientos con la camara",
        "Desarrollado por Diego P, TIMOTEO EN 3D",
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
    glTranslate(state.gato_x,0,state.gato_z)
    #glRotate(state.rotate_x,0,1,0)
    #glRotate(state.rotate_y,1,0,0)
    gato.draw_gato_full() # Dibuja el gato completo (cuerpo, patas, cabeza, boca, cola, collar)
    if state.show_instructions:
        show_menu()
        
    glutSwapBuffers()
    glPopMatrix()

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
    
    glutMainLoop()
   
if __name__ == "__main__":
    main()