from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

PINK = [0.91, 0.15, 0.45, 1.0]
BLACK = [0.11, 0.11, 0.11, 1.0]
BLUE = [0.10, 0.55, 0.90, 1.0]
RED = [0.9, 0.1, 0.1, 1.0]
BROWN = [0.55, 0.27, 0.07, 1.0]
PURPLE = [0.8, 0.2, 0.9, 1.0]

def setMaterial(color, is_shadow=False):
    """
    Si es sombra, ignoramos por completo cualquier solicitud de cambio de color.
    """
    if is_shadow:
        return 

    glColor3fv(color[:3])
    glMaterialfv(GL_FRONT, GL_AMBIENT, [color[0]*0.5, color[1]*0.5, color[2]*0.5, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

def draw_cylinder_between(p1, p2, radius, is_cone=False):
    x1, y1, z1 = p1; x2, y2, z2 = p2
    dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
    length = math.sqrt(dx*dx + dy*dy + dz*dz)
    glPushMatrix()
    glTranslatef(x1, y1, z1)
    if length > 0.0001:
        dx, dy, dz = dx/length, dy/length, dz/length
        cross_x = -dy; cross_y = dx; cross_z = 0.0
        cross_length = math.sqrt(cross_x**2 + cross_y**2)
        if cross_length < 0.0001:
            if dz < 0: glRotatef(180, 1, 0, 0)
        else:
            angle = math.degrees(math.acos(dz))
            glRotatef(angle, cross_x, cross_y, cross_z)
    quad = gluNewQuadric()
    top_radius = 0.0 if is_cone else radius
    gluCylinder(quad, radius, top_radius, length, 20, 20)
    gluDeleteQuadric(quad)
    glPopMatrix()

def draw_head(p, is_shadow):
    glPushMatrix()
    setMaterial(PINK, is_shadow)
    glTranslatef(0, 5, 0)
    glutSolidSphere(2.0, 40, 40)
    glPopMatrix()

    blink = math.sin(p.blink_timer) > 0.95
    for dx in [-0.6, 0.6]:
        glPushMatrix()
        glTranslatef(dx, 5.5, 1.85)
        if blink: glScalef(1.0, 0.1, 1.0)
        
        # Selección de color según expresión
        target_color = BLACK
        if p.expression == "angry": target_color = RED
        elif p.expression == "power": target_color = PURPLE
        
        setMaterial(target_color, is_shadow)
        
        if p.expression == "angry":
            glRotatef(-35 if dx < 0 else 35, 0, 0, 1)
            glScalef(1.5, 0.6, 1.0)
        elif p.expression == "power":
            glScalef(1.4, 1.4, 1.0)
        elif p.expression in ["surprised", "happy"]:
            glScalef(1.2, 1.2, 1.0)
        
        glutSolidSphere(0.15, 16, 16)
        glPopMatrix()

    # Boca / Detalles
    if p.expression == "surprised":
        setMaterial(BLUE, is_shadow)
        glPushMatrix()
        glTranslatef(0.0, 4.3, 1.88)
        glutSolidSphere(0.4, 16, 16)
        glPopMatrix()
    else:
        setMaterial(PURPLE if p.expression == "power" else BLUE, is_shadow)
        for i in range(16):
            t = -1.0 + (i * (2.0 / 15.0))
            x = 0.6 * t
            if p.expression == "sad": y = 4.4 - 0.7 * (t**2)
            elif p.expression == "angry": y = 4.5 - 1.0 * (t**2)
            elif p.expression == "happy": y = 4.2 + 1.2 * (t**2)
            elif p.expression == "power": y = 4.3 + math.sin(t * 15) * 0.1
            else: y = 4.3 + 0.4 * (t**2)
            val = max(0, 4.0 - (x**2) - ((y - 5.0)**2))
            z = math.sqrt(val)
            if z > 1.95: z = 1.95
            glPushMatrix()
            glTranslatef(x, y, z)
            glutSolidSphere(0.16, 16, 16)
            glPopMatrix()

def draw_body(is_shadow):
    glPushMatrix(); setMaterial(BLUE, is_shadow); glTranslatef(0, 2.5, 0); glScalef(1.5, 2.0, 1.5); glutSolidSphere(1.0, 32, 32); glPopMatrix()
    glPushMatrix(); setMaterial(BLACK, is_shadow); glTranslatef(0, 1.2, 0); glScalef(1.6, 1.2, 1.6); glutSolidSphere(1.0, 32, 32); glPopMatrix()

def draw_limbs(p, is_shadow):
    swing_arms = math.sin(p.animation_angle) * 1.5 if p.walking else 0.0
    swing_legs = math.sin(p.animation_angle) * 1.5 if p.walking else 0.0

    setMaterial(BLUE, is_shadow)
    draw_cylinder_between((1.5, 3.0, 0), (1.5, 0.5, swing_arms), 0.35)
    draw_cylinder_between((-1.5, 3.0, 0), (-1.5, 0.5, -swing_arms), 0.35)
    for x, z_offset in [(-1.5, -swing_arms), (1.5, swing_arms)]:
        glPushMatrix(); glTranslatef(x, 0.5, z_offset); glutSolidSphere(0.35, 16, 16); glPopMatrix()

    draw_cylinder_between((0.6, 1.0, 0), (0.6, -1.0, -swing_legs), 0.4)
    draw_cylinder_between((-0.6, 1.0, 0), (-0.6, -1.0, swing_legs), 0.4)
    setMaterial(PINK, is_shadow)
    glPushMatrix(); glTranslatef(0.6, -1.2, -swing_legs); glutSolidSphere(0.5, 20, 20); glPopMatrix()
    glPushMatrix(); glTranslatef(-0.6, -1.2, swing_legs); glutSolidSphere(0.5, 20, 20); glPopMatrix()

def draw_ak47(p, is_shadow):
    arm_lift = 0.0
    color_arma = [0.25, 0.25, 0.25, 1.0]

    if p.reaction_type == "lift":
        progress = math.sin(math.pi * p.reaction_timer / p.reaction_duration)
        arm_lift = 2.0 * progress
        color_arma = PURPLE

    swing_arms = math.sin(p.animation_angle) * 1.5 if p.walking else 0.0
    
    glPushMatrix()
    glTranslatef(1.5, 0.5 + arm_lift, swing_arms)
    
    setMaterial(BROWN, is_shadow)
    draw_cylinder_between((0, 0, -0.5), (0, -0.8, -0.5), 0.15)
    draw_cylinder_between((0, 0, -1.5), (0, -0.5, -3.0), 0.25, is_cone=True)

    setMaterial(color_arma, is_shadow)
    draw_cylinder_between((0, 0, -1.5), (0, 0, 1.5), 0.25)
    draw_cylinder_between((0, 0, 1.5), (0, 0, 4.0), 0.1)
    draw_cylinder_between((0, 0.25, 1.5), (0, 0.25, 3.0), 0.12)
    draw_cylinder_between((0, -0.1, -0.2), (0, -1.5, 0.2), 0.18)
    glPushMatrix(); glTranslatef(0, 0.25, 3.8); glutSolidSphere(0.08, 10, 10); glPopMatrix()
    glPopMatrix()

def draw_metetoro_full(p):
    is_shadow = getattr(p, 'is_shadow_pass', False)

    glPushMatrix()
    glRotatef(p.direction_angle, 0, 1, 0)

    if p.walking:
        bounce = abs(math.sin(p.animation_angle)) * 0.15
        glTranslatef(0, bounce, 0)
        
    if p.reaction_type == "jump":
        y_offset = math.sin(math.pi * p.reaction_timer / p.reaction_duration) * 1.5
        glTranslatef(0, y_offset, 0)
    elif p.reaction_type == "spin":
        angle = 360 * (p.reaction_timer / p.reaction_duration)
        glTranslatef(0, 1.5, 0)
        glRotatef(angle, 0, 1, 0)
        glTranslatef(0, -1.5, 0)
    elif p.reaction_type == "shake":
        x_offset = math.sin(p.reaction_timer * 0.8 * math.pi) * 0.2
        glTranslatef(x_offset, 0, 0)

    glScalef(0.3, 0.3, 0.3)
    glTranslatef(0.0, 1.5, 0.0)

    if is_shadow:
        glDisable(GL_LIGHTING)
        # FORZAMOS EL COLOR NEGRO AQUÍ
        glColor4f(0.0, 0.0, 0.0, 0.8) 
        
        draw_body(True)
        draw_head(p, True)
        draw_limbs(p, True)
        draw_ak47(p, True)
        glEnable(GL_LIGHTING)
    else:
        draw_body(False)
        draw_head(p, False)
        draw_limbs(p, False)
        draw_ak47(p, False)
    
    glPopMatrix()