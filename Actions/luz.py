# lighting.py
from OpenGL.GL import *
from Actions import state

# Variable globale para la luz
light_pos = [5.0, 10.0, 5.0, 1.0]

def setup_lighting():
    global light_pos
    light_ambient = [0.2, 0.2, 0.2, 1.0]
    light_diffuse = [0.8, 0.8, 0.8, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    # Configuración de Material para simular brillo phon
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 60.0) 
def apply_light_position():
    global light_pos
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

def get_shadow_matrix():
    global light_pos
    Lx, Ly, Lz, Lw = light_pos 
    # Plano Y=0: A=0, B=1, C=0, D=0
    A, B, C, D = 0.0, 1.0, 0.0, 0.0
    dot = A*Lx + B*Ly + C*Lz + D*Lw 
    mat = [
        dot - Lx*A, -Ly*A,      -Lz*A,      -Lw*A,
        -Lx*B,      dot - Ly*B, -Lz*B,      -Lw*B,
        -Lx*C,      -Ly*C,      dot - Lz*C, -Lw*C,
        -Lx*D,      -Ly*D,      -Lz*D,      dot - Lw*D
    ]
    return mat

def set_color(r, g, b, a=1.0):
    if state.is_shadow_pass:
        glColor4f(0.05, 0.05, 0.05, 0.6) # Color de la sombra
    else:
        glColor4f(r, g, b, a)

def apply_shading():
    # GL_FLAT = Sombreado Plano, GL_SMOOTH = Sombreado Gouraud
    if state.shading_mode == "Flat":
        glShadeModel(GL_FLAT)
    else:
        glShadeModel(GL_SMOOTH)

def toggle_shading():
    if state.shading_mode == "Gouraud":
        state.shading_mode = "Flat"
    else:
        state.shading_mode = "Gouraud"

def setup_lighting():
    global light_pos
    # Bajamos la ambiental para que el foco resalte (Look dramático)
    light_ambient = [0.1, 0.1, 0.1, 1.0] 
    # Luz difusa con un tono azulado frío (Estilo Tech/Halcón)
    light_diffuse = [0.9, 0.9, 1.0, 1.0] 
    light_specular = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

    # reflector
    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 25.0)      # Ángulo del foco (cono)
    glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 15.0)    # Concentración en el centro
    
    # Material con más brillo (Shininess) para resaltar los polígonos
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 80.0) 

def update_spotlight(target_x):

    # La luz se mueve en X para seguir al personaje
    dynamic_light_pos = [target_x, 10.0, 5.0, 1.0]
    # Dirección apuntando hacia abajo directamente al modelo
    direction = [0.0, -1.0, -0.2] 
    
    glLightfv(GL_LIGHT0, GL_POSITION, dynamic_light_pos)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, direction)