from OpenGL.GL import *
from core.constants import WINDOW_WIDTH, WINDOW_HEIGHT

def setup_viewport(width, height):
    """Configures the viewport and sets a 2D orthographic coordinate system."""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    glOrtho(0, width, height, 0, -1, 1)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()