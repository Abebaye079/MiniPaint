from OpenGL.GL import *
from core.constants import BG_COLOR

class Renderer:
    def __init__(self):
        glClearColor(*BG_COLOR)

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def render_scene(self, shape_manager):
        """Main render calls happen here."""
        self.clear()
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity() 

        shape_manager.draw_all()
        
        glFlush()
