from OpenGL.GL import *
import math
from Utils.dibujar_cubo import draw_cube

class CollisionObject:
    def __init__(self, x, z, size=1.0, color=(0.5, 0.5, 0.5), label="objeto", 
                 expresion="neutral", animacion=None, sonido="meow", width=None, depth=None, shape="cube"):
        self.x = x
        self.z = z
        self.size = size
        self.width = width if width is not None else size
        self.depth = depth if depth is not None else size
        self.color = color
        self.label = label
        self.expresion = expresion
        self.animacion = animacion
        self.sonido = sonido
        self.shape = shape

    def draw(self):
        glPushMatrix()
        glColor3f(*self.color)
        if self.shape == "sphere":
            from OpenGL.GLUT import glutSolidSphere
            glTranslatef(self.x, self.size / 2, self.z)
            glutSolidSphere(self.size / 2, 16, 16)
        else:
            half_w = self.width / 2
            half_d = self.depth / 2
            draw_cube(self.x - half_w, 0, self.z - half_d,
                      self.x + half_w, self.size, self.z + half_d)
        glPopMatrix()

    def check_collision(self, gato_x, gato_z, threshold=1.2, gato_y=0.0):
        gato_margen = threshold / 2
        half_w = self.width / 2
        half_d = self.depth / 2
        colision_x = abs(gato_x - self.x) < (gato_margen + half_w)
        colision_z = abs(gato_z - self.z) < (gato_margen + half_d)
        colision_y = gato_y < self.size
        return colision_x and colision_z and colision_y
