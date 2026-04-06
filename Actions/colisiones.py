from OpenGL.GL import *
import math
from Utils.dibujar_cubo import draw_cube

class CollisionObject:
    def __init__(self, x, z, size=1.0, color=(0.5, 0.5, 0.5), label="objeto"):
        self.x = x
        self.z = z
        self.size = size
        self.color = color
        self.label = label

    def draw(self):
        glPushMatrix()
        glColor3f(*self.color)
        # Dibujamos el objeto centrado en su posición
        draw_cube(self.x - self.size/2, 0, self.z - self.size/2,
                  self.x + self.size/2, self.size, self.z + self.size/2)
        glPopMatrix()

    def check_collision(self, gato_x, gato_z, threshold=1.2):
        dist = math.sqrt((gato_x - self.x)**2 + (gato_z - self.z)**2)
        return dist < threshold