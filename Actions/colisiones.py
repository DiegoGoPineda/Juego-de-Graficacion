from OpenGL.GL import *
import math
from Utils.dibujar_cubo import draw_cube
class CollisionObject:
    def __init__(self, x, z, size=1.0, color=(0.5, 0.5, 0.5), label="objeto", 
                 expresion="neutral", animacion=None, sonido="meow"):
        self.x = x
        self.z = z
        self.size = size
        self.color = color
        self.label = label
        # atributos para mejorar las colisiones
        self.expresion = expresion
        self.animacion = animacion
        self.sonido = sonido

    def draw(self):
        glPushMatrix()
        glColor3f(*self.color)
        half = self.size / 2
        draw_cube(self.x - half, 0, self.z - half,
                  self.x + half, self.size, self.z + half)
        glPopMatrix()

    def check_collision(self, gato_x, gato_z, threshold=1.2): 
        gato_margen = threshold / 2 
        obj_margen = self.size / 2
        colision_x = abs(gato_x - self.x) < (gato_margen + obj_margen)
        colision_z = abs(gato_z - self.z) < (gato_margen + obj_margen)
        return colision_x and colision_z


    