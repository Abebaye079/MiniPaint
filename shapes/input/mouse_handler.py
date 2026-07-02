import glfw
from shapes.line import Line
from shapes.polyline import Polyline
from shapes.polygon import Polygon

class MouseHandler:
    def __init__(self, shape_manager):
        self.shape_manager = shape_manager
        self.start_pos = None
        self.current_tool = "line"
        self.temp_points = []  # Accumulates points for multi-point shapes

    def set_tool(self, tool_name):
        # Clear any half-drawn shapes when switching tools
        self.temp_points.clear()
        self.start_pos = None
        self.current_tool = tool_name

    def mouse_button_callback(self, window, button, action, mods):
        x, y = glfw.get_cursor_pos(window)
        print(f"Mouse clicked! Button: {button}, Action: {action}, Tool: {self.current_tool}")

        # ---- LEFT CLICK: DRAWING / ADDING POINTS ----
        if button == glfw.MOUSE_BUTTON_LEFT:
            # LINE TOOL (Click, Drag, and Release)
            if self.current_tool == "line":
                if action == glfw.PRESS:
                    self.start_pos = (x, y)
                elif action == glfw.RELEASE and self.start_pos:
                    line = Line(self.start_pos, (x, y))
                    self.shape_manager.add_shape(line)
                    self.start_pos = None

            # POLYLINE & POLYGON TOOLS (Accumulate points on click)
            elif self.current_tool in ["polyline", "polygon"]:
                if action == glfw.PRESS:
                    self.temp_points.append((x, y))

        # ---- RIGHT CLICK: FINALIZE MULTI-POINT SHAPES ----
        elif button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.PRESS:
            if self.current_tool == "polyline" and len(self.temp_points) >= 2:
                polyline = Polyline(self.temp_points.copy())
                self.shape_manager.add_shape(polyline)
                self.temp_points.clear()

            elif self.current_tool == "polygon" and len(self.temp_points) >= 3:
                polygon = Polygon(self.temp_points.copy())
                self.shape_manager.add_shape(polygon)
                self.temp_points.clear()
