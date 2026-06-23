from OpenGL.GL import *
from shapes.shape import Shape

class Line(Shape):
    def __init__(self, p1, p2, color=(1, 0, 0)):
        super().__init__(color)
        self.vertices = [p1, p2]

    def draw(self):
        glPushMatrix()  # Isolate this shape's matrix state
        self.apply_opengl_transforms()

        glColor3f(*self.color)
        glBegin(GL_LINES)
        glVertex2f(*self.vertices[0])
        glVertex2f(*self.vertices[1])
        glEnd()

        glPopMatrix()  # Restore previous matrix state for other shapes

