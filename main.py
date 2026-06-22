import glfw
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from OpenGL.GL import *
from core.constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from core.viewport import setup_viewport
from core.renderer import Renderer
from shapes.shape_manager import ShapeManager

def mouse_button_callback(window, button, action, mods):
    """Callback for mouse clicks."""
    if action == glfw.PRESS:
        x, y = glfw.get_cursor_pos(window)
        print(f"Mouse Clicked at Screen Position: ({x}, {y})")

def key_callback(window, key, scancode, action, mods):
    """Callback for keyboard inputs."""
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

def window_size_callback(window, width, height):
    """Ensures viewport updates properly when the window is resized."""
    setup_viewport(width, height)

def main():
    if not glfw.init():
        sys.exit("Failed to initialize GLFW")

    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, None, None)
    if not window:
        glfw.terminate()
        sys.exit("Failed to create GLFW window")

    glfw.make_context_current(window)
    
    setup_viewport(WINDOW_WIDTH, WINDOW_HEIGHT)
    renderer = Renderer()
    shape_manager = ShapeManager()

    glfw.set_window_size_callback(window, window_size_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        renderer.render_scene(shape_manager)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()