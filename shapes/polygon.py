from OpenGL.GL import *
from shapes.shape import Shape

class Polygon(Shape):
    def __init__(self, points=None, color=(0, 1, 0)):
        super().__init__(color)
        self.vertices = points if points else []

    def add_point(self, point):
        self.vertices.append(point)

    def draw(self):
        if len(self.vertices) < 3:
            return

        glPushMatrix()  # Isolate matrix state
        self.apply_opengl_transforms()

        glColor3f(*self.color)
        glBegin(GL_POLYGON)
        for x, y in self.vertices:
            glVertex2f(x, y)
        glEnd()

        glPopMatrix()  # Restore matrix state

