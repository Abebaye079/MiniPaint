import glfw

class KeyboardHandler:
    """
    Handles keyboard input for tool switching, transformations, and utilities.
    
    Wired to:
    - mouse_handler: for tool switching (L, P, G, S)
    - selection_manager: for entering selection mode (S) and deleting shapes (Delete)
    - transform_manager: for transformations on selected shapes (arrows, brackets, +/-)
    - shape_manager: for clearing canvas (C)
    
    TOOL SWITCHING:
    - L: Line Tool
    - P: Polyline Tool
    - G: Polygon Tool
    - S: Selection Mode
    
    TRANSFORMATIONS (on selected shape):
    - Arrow Keys: Move (Up, Down, Left, Right)
    - [ ]: Rotate counter-clockwise / clockwise
    - + / -: Scale up / down
    - R: Reset transform
    
    UTILITIES:
    - Delete: Remove selected shape
    - C: Clear canvas
    - ESC: Already handled in main, but can be extended here if needed
    """
    
    def __init__(self, mouse_handler, selection_manager, transform_manager, shape_manager):
        self.mouse_handler = mouse_handler
        self.selection_manager = selection_manager
        self.transform_manager = transform_manager
        self.shape_manager = shape_manager
        
        # Current mode tracking
        self.selection_mode = False
    
    def key_callback(self, window, key, scancode, action, mods):
        """Main keyboard callback. Only responds to KEY_PRESS."""
        if action != glfw.PRESS:
            return
        
        # ===== TOOL SWITCHING =====
        if key == glfw.KEY_L:
            self._switch_tool("line")
        elif key == glfw.KEY_P:
            self._switch_tool("polyline")
        elif key == glfw.KEY_G:
            self._switch_tool("polygon")
        elif key == glfw.KEY_S:
            self._toggle_selection_mode()
        
        # ===== TRANSFORMATIONS (only if a shape is selected) =====
        elif key == glfw.KEY_UP:
            self.transform_manager.move_up()
        elif key == glfw.KEY_DOWN:
            self.transform_manager.move_down()
        elif key == glfw.KEY_LEFT:
            self.transform_manager.move_left()
        elif key == glfw.KEY_RIGHT:
            self.transform_manager.move_right()
        
        # Rotation: [ = CCW, ] = CW
        elif key == glfw.KEY_LEFT_BRACKET:
            self.transform_manager.rotate_ccw()
        elif key == glfw.KEY_RIGHT_BRACKET:
            self.transform_manager.rotate_cw()
        
        # Scaling: + = grow, - = shrink
        elif key == glfw.KEY_EQUAL:  # = key and + key (with Shift)
            self.transform_manager.scale_up()
        elif key == glfw.KEY_MINUS:  # - key
            self.transform_manager.scale_down()
        
        # Reset: R
        elif key == glfw.KEY_R:
            self.transform_manager.reset_transform()
        
        # ===== UTILITIES =====
        elif key == glfw.KEY_DELETE:
            self._delete_selected()
        elif key == glfw.KEY_C:
            self._clear_canvas()
        
        # ESC is already handled in main.py, but we can extend here if needed
        elif key == glfw.KEY_ESCAPE:
            # Optionally exit selection mode or clear selection
            if self.selection_mode:
                self._exit_selection_mode()
    
    # ===== TOOL SWITCHING HELPERS =====
    
    def _switch_tool(self, tool_name):
        """Switch the current drawing tool."""
        self.mouse_handler.set_tool(tool_name)
        print(f"[Keyboard] Tool switched to: {tool_name}")
    
    def _toggle_selection_mode(self):
        """Toggle between drawing and selection mode."""
        if self.selection_mode:
            self._exit_selection_mode()
        else:
            self._enter_selection_mode()
    
    def _enter_selection_mode(self):
        """Enter selection mode (prevents accidental drawing)."""
        self.selection_mode = True
        self.mouse_handler.set_tool("selection")
        print("[Keyboard] Entered SELECTION MODE. Click shapes to select.")
    
    def _exit_selection_mode(self):
        """Exit selection mode and return to last drawing tool."""
        self.selection_mode = False
        self.mouse_handler.set_tool("line")
        self.selection_manager.clear_selection()
        print("[Keyboard] Exited selection mode. Switched to line tool.")
    
    # ===== UTILITY HELPERS =====
    
    def _delete_selected(self):
        """Delete the currently selected shape."""
        selected = self.selection_manager.get_selected_shape()
        if selected:
            self.shape_manager.remove_shape(selected)
            self.selection_manager.clear_selection()
            print("[Keyboard] Deleted selected shape.")
        else:
            print("[Keyboard] No shape selected to delete.")
    
    def _clear_canvas(self):
        """Clear all shapes from the canvas."""
        self.shape_manager.clear()
        self.selection_manager.clear_selection()
        print("[Keyboard] Canvas cleared.")
