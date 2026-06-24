import glfw
import sys
import os
import math

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from core.viewport import setup_viewport
from core.renderer import Renderer
from shapes.shape_manager import ShapeManager
from shapes.input.mouse_handler import MouseHandler
from selection.selection_manager import SelectionManager
from transform.transform_manager import TransformManager
from ui.ui_manager import UIManager
from input.keyboard_handler import KeyboardHandler

# Import shapes for testing
from shapes.line import Line
from shapes.polygon import Polygon

# Global UI and Handler references for the unified mouse callback
ui_manager = None
mouse_handler = None
selection_manager = None

def mouse_callback(window, button, action, mods):
    """
    Unified mouse callback that prioritizes UI interaction,
    then selection, then drawing.
    """
    global ui_manager, mouse_handler, selection_manager
    mx, my = glfw.get_cursor_pos(window)

    # 1. UI takes priority (e.g. clicking a color swatch)
    if ui_manager and ui_manager.handle_mouse_click(mx, my, button, action):
        return

    # 2. Selection tool logic
    if ui_manager and ui_manager.current_tool == "selection":
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            selection_manager.select(mx, my)
        return

    # 3. Canvas drawing logic
    if mouse_handler:
        mouse_handler.mouse_button_callback(window, button, action, mods)

def window_size_callback(window, width, height):
    """Update viewport and UI dimensions on resize."""
    setup_viewport(width, height)
    global ui_manager
    if ui_manager:
        ui_manager.screen_width = width
        ui_manager.screen_height = height
        # Note: UI positions like status bar might need re-init if they are fixed at bottom
        # For simplicity in this demo, we just update the stored dimensions.

def main():
    global ui_manager, mouse_handler, selection_manager

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
    transform_manager = TransformManager()
    selection_manager = SelectionManager(shape_manager, transform_manager)
    ui_manager = UIManager(WINDOW_WIDTH, WINDOW_HEIGHT)

    # Connect UI Manager
    ui_manager.set_shape_manager(shape_manager)
    ui_manager.set_selection_manager(selection_manager)
    ui_manager.set_transform_manager(transform_manager)

    # Handlers
    mouse_handler = MouseHandler(shape_manager)
    keyboard_handler = KeyboardHandler(
        mouse_handler,
        selection_manager,
        transform_manager,
        shape_manager,
        ui_manager
    )

    # Register callbacks
    glfw.set_window_size_callback(window, window_size_callback)
    glfw.set_mouse_button_callback(window, mouse_callback)
    glfw.set_key_callback(window, keyboard_handler.key_callback)

    # ===== TEST SHAPES =====
    static_line = Line((50, 50), (200, 50), color=(0, 0, 0))
    shape_manager.add_shape(static_line)

    test_poly = Polygon([(0, -50), (50, 50), (-50, 50)], color=(1, 0, 0))
    test_poly.transform.tx = 400
    test_poly.transform.ty = 300
    shape_manager.add_shape(test_poly)

    # Main loop
    while not glfw.window_should_close(window):
        glfw.poll_events()

        # --- UPDATE ---
        mx, my = glfw.get_cursor_pos(window)
        ui_manager.update(mx, my)

        # Simple animation for the test triangle
        test_poly.transform.rotation += 0.5

        # --- RENDER ---
        # 1. Clear and Draw Shapes
        renderer.render_scene(shape_manager)

        # 2. Draw UI Overlay (HUD, Panels, Help)
        ui_manager.draw()

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
