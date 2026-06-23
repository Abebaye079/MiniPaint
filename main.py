import glfw
import sys
import os
import math  # Added for pulsation math

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from core.viewport import setup_viewport
from core.renderer import Renderer
from shapes.shape_manager import ShapeManager
from shapes.input.mouse_handler import MouseHandler

# Temporarily import shapes to perform Israel's Transformation Test
from shapes.line import Line
from shapes.polygon import Polygon

def key_callback(window, key, scancode, action, mods):
    """Exit on ESC key."""
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

def window_size_callback(window, width, height):
    """Update viewport on resize."""
    setup_viewport(width, height)

def main():
    global mouse_handler

    if not glfw.init():
        sys.exit("Failed to initialize GLFW")

    window = glfw.create_window(
        WINDOW_WIDTH,
        WINDOW_HEIGHT,
        WINDOW_TITLE,
        None,
        None
    )

    if not window:
        glfw.terminate()
        sys.exit("Failed to create GLFW window")

    glfw.make_context_current(window)

    # Core systems
    setup_viewport(WINDOW_WIDTH, WINDOW_HEIGHT)

    renderer = Renderer()
    shape_manager = ShapeManager()

    # Mouse system
    mouse_handler = MouseHandler(shape_manager)

    # Callbacks
    glfw.set_window_size_callback(window, window_size_callback)
    glfw.set_mouse_button_callback(window, mouse_handler.mouse_button_callback)
    glfw.set_key_callback(window, key_callback)

    # =================================================================
    # --- ISRAEL'S TRANSFORMATION SYSTEM VERIFICATION TEST ---
    # =================================================================
    
    # Test Shape 1: A static reference line (Black)
    # This proves other shapes aren't accidentally affected by global matrix leaks.
    static_line = Line((50, 50), (200, 50), color=(0, 0, 0))
    shape_manager.add_shape(static_line)

    # Test Shape 2: A test triangle (Red) centered at local (0, 0) relative to its origin
    test_poly = Polygon([(0, -50), (50, 50), (-50, 50)], color=(1, 0, 0))
    
    # Place its initial transform position right in the middle of your 800x600 screen
    test_poly.transform.tx = 400 
    test_poly.transform.ty = 300
    
    shape_manager.add_shape(test_poly)
    
    # =================================================================

    # Main loop
    while not glfw.window_should_close(window):
        glfw.poll_events()

        # --- LIVE ANIMATION UPDATE PASS ---
        # 1. Rotate the triangle continuously over time (updates transform.rotation)
        test_poly.transform.rotation += 1.0
        if test_poly.transform.rotation >= 360.0:
            test_poly.transform.rotation = 0.0

        # 2. Pulsate the scale factors smoothly over time (updates transform.sx and sy)
        current_time = glfw.get_time()
        pulse_factor = 1.0 + 0.3 * math.sin(current_time * 3)  # Loops between 0.7 and 1.3
        test_poly.transform.sx = pulse_factor
        test_poly.transform.sy = pulse_factor

        # Render everything
        renderer.render_scene(shape_manager)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
 
