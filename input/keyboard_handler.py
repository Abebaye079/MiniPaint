import glfw

class KeyboardHandler:
    """
    Handles keyboard input for tool switching, transformations, and utilities.
    """
    
    def __init__(self, mouse_handler, selection_manager, transform_manager, shape_manager, ui_manager):
        self.mouse_handler = mouse_handler
        self.selection_manager = selection_manager
        self.transform_manager = transform_manager
        self.shape_manager = shape_manager
        self.ui_manager = ui_manager
        
        # Current mode tracking
        self.selection_mode = False
        
        # Color mapping (numbers to color names)
        self.color_map = {
            glfw.KEY_1: "Red",
            glfw.KEY_2: "Green",
            glfw.KEY_3: "Blue",
            glfw.KEY_4: "Yellow",
            glfw.KEY_5: "Cyan",
            glfw.KEY_6: "Magenta",
            glfw.KEY_7: "White",
            glfw.KEY_8: "Black",
            glfw.KEY_9: "Orange",
            glfw.KEY_0: "Purple"
        }
        
        # Tool mapping
        self.tool_map = {
            glfw.KEY_L: "line",
            glfw.KEY_P: "polyline",
            glfw.KEY_G: "polygon",
            glfw.KEY_S: "selection"
        }
    
    def key_callback(self, window, key, scancode, action, mods):
        """Main keyboard callback. Only responds to KEY_PRESS."""
        if action != glfw.PRESS:
            return
        
        # ===== TOOL SWITCHING =====
        if key in self.tool_map:
            tool_name = self.tool_map[key]
            self.ui_manager.set_tool(tool_name)
            self.mouse_handler.set_tool(tool_name)
            
            # Update selection mode state
            if tool_name == "selection":
                self.selection_mode = True
                print(f"[Keyboard] Entered SELECTION MODE")
            else:
                self.selection_mode = False
                if self.selection_manager:
                    self.selection_manager.clear_selection()
                    self.ui_manager.set_selected_shape(None)
                print(f"[Keyboard] Tool switched to: {tool_name}")
        
        # ===== COLOR SELECTION =====
        elif key in self.color_map:
            color_name = self.color_map[key]
            if self.ui_manager.select_color_by_name(color_name):
                print(f"[Keyboard] Selected color: {color_name}")
                # Update shape manager's current color if it has one
                if hasattr(self.shape_manager, 'current_color'):
                    self.shape_manager.current_color = self.ui_manager.get_current_color()
        
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
            print("[Keyboard] Transform reset")
        
        # ===== UTILITIES =====
        elif key == glfw.KEY_DELETE:
            if self.ui_manager.delete_selected_shape():
                print("[Keyboard] Deleted selected shape.")
            else:
                print("[Keyboard] No shape selected to delete.")
        
        elif key == glfw.KEY_C:
            self.ui_manager.clear_canvas()
            print("[Keyboard] Canvas cleared.")
        
        elif key == glfw.KEY_H:
            help_visible = self.ui_manager.toggle_help()
            print(f"[Keyboard] Help menu: {'shown' if help_visible else 'hidden'}")
        
        # ESC is already handled in main.py