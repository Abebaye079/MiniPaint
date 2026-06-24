from OpenGL.GL import *
from OpenGL.GLUT import *
import glfw
import math

# Initialize GLUT for text rendering
try:
    glutInit()
except:
    pass

class UIComponent:
    """Base class for all UI elements."""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        self.enabled = True
        self.is_hovered = False

    def contains(self, mx, my):
        return self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height

    def draw(self):
        pass

    def handle_hover(self, mx, my):
        if not self.visible or not self.enabled:
            self.is_hovered = False
            return False
        self.is_hovered = self.contains(mx, my)
        return self.is_hovered

    def handle_click(self, mx, my):
        if not self.visible or not self.enabled:
            return False
        return self.contains(mx, my)

class Panel(UIComponent):
    """A container with a background and optional border."""
    def __init__(self, x, y, width, height, bg_color=(0.1, 0.1, 0.18, 0.85), border_color=(0.3, 0.3, 0.5, 1.0)):
        super().__init__(x, y, width, height)
        self.bg_color = bg_color
        self.border_color = border_color
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def draw(self):
        if not self.visible: return

        # Draw background
        glColor4f(*self.bg_color)
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

        # Draw border
        glColor4f(*self.border_color)
        glLineWidth(1.5)
        glBegin(GL_LINE_LOOP)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

        for child in self.children:
            child.draw()

class Label(UIComponent):
    """Text label using GLUT bitmap fonts."""
    def __init__(self, x, y, text, color=(1, 1, 1, 1), font=GLUT_BITMAP_HELVETICA_12):
        super().__init__(x, y, 0, 0)
        self.text = text
        self.color = color
        self.font = font

    def draw(self):
        if not self.visible: return
        glColor4f(*self.color)
        # GLUT bitmap fonts use raster position. We offset for baseline.
        glRasterPos2f(self.x, self.y + 12)
        for char in self.text:
            glutBitmapCharacter(self.font, ord(char))

class Button(UIComponent):
    """Interactive button."""
    def __init__(self, x, y, width, height, text, callback=None, bg_color=(0.2, 0.2, 0.3, 1.0)):
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback
        self.bg_color = bg_color
        self.accent_color = (0.4, 0.4, 0.8, 1.0)

    def draw(self):
        if not self.visible: return
        color = self.accent_color if self.is_hovered else self.bg_color
        glColor4f(*color)
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

        glColor4f(1, 1, 1, 0.5)
        glBegin(GL_LINE_LOOP)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

        glColor4f(1, 1, 1, 1)
        text_x = self.x + (self.width - len(self.text) * 7) / 2
        glRasterPos2f(text_x, self.y + (self.height + 10) / 2)
        for char in self.text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))

    def handle_click(self, mx, my):
        if super().handle_click(mx, my):
            if self.callback: self.callback()
            return True
        return False

class UIManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_tool = "line"
        self.current_color = (1.0, 0.0, 0.0)
        self.shape_manager = None
        self.selection_manager = None
        self.transform_manager = None
        self.show_help = False

        self.colors = {
            "Red": (1.0, 0.0, 0.0), "Green": (0.0, 1.0, 0.0), "Blue": (0.0, 0.0, 1.0),
            "Yellow": (1.0, 1.0, 0.0), "Cyan": (0.0, 1.0, 1.0), "Magenta": (1.0, 0.0, 1.0),
            "White": (1.0, 1.0, 1.0), "Black": (0.0, 0.0, 0.0), "Orange": (1.0, 0.5, 0.0),
            "Purple": (0.5, 0.0, 1.0)
        }
        self.color_names = list(self.colors.keys())
        self.current_color_index = 0

        self.panels = []
        self._init_ui()

    def _init_ui(self):
        # Tool Panel (Top Left)
        self.tool_panel = Panel(10, 10, 200, 80)
        self.tool_label = Label(20, 15, "TOOL: LINE", (1, 0.8, 0, 1), GLUT_BITMAP_HELVETICA_18)
        self.tool_panel.add_child(self.tool_label)
        self.shape_count_label = Label(20, 45, "Shapes: 0")
        self.tool_panel.add_child(self.shape_count_label)
        self.shortcut_label = Label(20, 62, "L, P, G, S to switch", (0.7, 0.7, 0.7, 1))
        self.tool_panel.add_child(self.shortcut_label)
        self.panels.append(self.tool_panel)

        # Color Palette (Top Right)
        self.palette_panel = Panel(self.screen_width - 190, 10, 180, 95)
        self.color_name_label = Label(self.screen_width - 180, 70, "Color: Red")
        self.palette_panel.add_child(self.color_name_label)
        self.panels.append(self.palette_panel)

        # Transform Panel (Bottom Right)
        self.transform_panel = Panel(self.screen_width - 210, self.screen_height - 180, 200, 130)
        self.transform_panel.visible = False
        self.panels.append(self.transform_panel)

        # Status Bar (Bottom)
        self.status_bar = Panel(0, self.screen_height - 40, self.screen_width, 40, bg_color=(0.05, 0.05, 0.1, 0.9))
        self.status_label = Label(15, self.screen_height - 35, "Ready")
        self.status_bar.add_child(self.status_label)
        self.mouse_pos_label = Label(self.screen_width - 150, self.screen_height - 35, "0, 0")
        self.status_bar.add_child(self.mouse_pos_label)
        self.panels.append(self.status_bar)

    def set_shape_manager(self, sm): self.shape_manager = sm
    def set_selection_manager(self, sel): self.selection_manager = sel
    def set_transform_manager(self, tm): self.transform_manager = tm

    def set_tool(self, tool):
        self.current_tool = tool
        self.tool_label.text = f"TOOL: {tool.upper()}"
        self.status_label.text = f"Mode: {tool.capitalize()}"

    def select_color_by_name(self, name):
        if name in self.colors:
            self.current_color = self.colors[name]
            self.current_color_index = self.color_names.index(name)
            self.color_name_label.text = f"Color: {name}"
            return True
        return False

    def toggle_help(self):
        self.show_help = not self.show_help
        return self.show_help

    def update(self, mx, my):
        # Update text values
        self.mouse_pos_label.text = f"X: {int(mx)} Y: {int(my)}"
        if self.shape_manager:
            self.shape_count_label.text = f"Shapes: {len(self.shape_manager.shapes)}"

        # Display transformations for selected shape
        if self.selection_manager and self.selection_manager.has_selection():
            shape = self.selection_manager.get_selected_shape()
            self.transform_panel.visible = True
            self.transform_panel.children = [
                Label(self.transform_panel.x + 10, self.transform_panel.y + 10, f"SELECTED: {type(shape).__name__}", (0.4, 1, 0.4, 1)),
                Label(self.transform_panel.x + 10, self.transform_panel.y + 40, f"Pos: ({int(shape.transform.tx)}, {int(shape.transform.ty)})"),
                Label(self.transform_panel.x + 10, self.transform_panel.y + 65, f"Rot: {int(shape.transform.rotation)} deg"),
                Label(self.transform_panel.x + 10, self.transform_panel.y + 90, f"Scale: {shape.transform.sx:.2f}x")
            ]
        else:
            self.transform_panel.visible = False

        # Handle hover states
        for p in self.panels:
            p.handle_hover(mx, my)

    def handle_mouse_click(self, mx, my, button, action):
        if action != glfw.PRESS: return False

        # Check color palette clicks
        if self.palette_panel.contains(mx, my):
            start_x = self.screen_width - 180
            start_y = 20
            for i in range(10):
                row, col = divmod(i, 5)
                bx, by = start_x + col * 32, start_y + row * 22
                if bx <= mx <= bx + 28 and by <= my <= by + 18:
                    self.select_color_by_name(self.color_names[i])
                    return True
        return False

    def draw_palette_swatches(self):
        start_x = self.screen_width - 180
        start_y = 20
        for i, name in enumerate(self.color_names):
            row, col = divmod(i, 5)
            color = self.colors[name]
            bx, by = start_x + col * 32, start_y + row * 22

            # Draw highlight for selected color
            if i == self.current_color_index:
                glColor4f(1, 1, 1, 1)
                glLineWidth(2)
                glBegin(GL_LINE_LOOP)
                glVertex2f(bx-2, by-2); glVertex2f(bx+30, by-2)
                glVertex2f(bx+30, by+20); glVertex2f(bx-2, by+20)
                glEnd()

            glColor3f(*color)
            glBegin(GL_QUADS)
            glVertex2f(bx, by); glVertex2f(bx+28, by)
            glVertex2f(bx+28, by+18); glVertex2f(bx, by+18)
            glEnd()

    def draw_help_menu(self):
        if not self.show_help: return

        # Dim background
        glColor4f(0, 0, 0, 0.75)
        glBegin(GL_QUADS)
        glVertex2f(0, 0); glVertex2f(self.screen_width, 0)
        glVertex2f(self.screen_width, self.screen_height); glVertex2f(0, self.screen_height)
        glEnd()

        # Center modal
        help_panel = Panel(self.screen_width//2 - 250, self.screen_height//2 - 210, 500, 420, (0.1, 0.1, 0.2, 0.95))
        help_panel.draw()

        y_off = help_panel.y + 20
        texts = [
            ("HELP MENU", (1, 0.8, 0, 1), GLUT_BITMAP_HELVETICA_18),
            ("", None, None),
            ("TOOLS: L: Line, P: Polyline, G: Polygon, S: Selection", (1, 1, 1, 1), GLUT_BITMAP_HELVETICA_12),
            ("COLORS: Keys 1-9, 0", (1, 1, 1, 1), GLUT_BITMAP_HELVETICA_12),
            ("TRANSFORMS (Selection Mode):", (0.5, 0.8, 1, 1), GLUT_BITMAP_HELVETICA_12),
            ("  Arrows: Move, [ ]: Rotate, +/-: Scale, R: Reset", (1, 1, 1, 1), GLUT_BITMAP_HELVETICA_12),
            ("", None, None),
            ("ACTIONS: Delete: Remove, C: Clear, H: Toggle Help", (1, 1, 1, 1), GLUT_BITMAP_HELVETICA_12),
            ("", None, None),
            ("Press 'H' to close", (0.7, 0.7, 0.7, 1), GLUT_BITMAP_HELVETICA_12)
        ]

        for text, color, font in texts:
            if text:
                glColor4f(*color)
                glRasterPos2f(help_panel.x + 30, y_off + 15)
                for char in text: glutBitmapCharacter(font, ord(char))
            y_off += 25

    def draw(self):
        # Switch to Ortho for UI rendering
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.screen_width, self.screen_height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Draw all panels
        for p in self.panels:
            p.draw()

        self.draw_palette_swatches()
        self.draw_help_menu()

        glDisable(GL_BLEND)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def delete_selected_shape(self):
        if self.selection_manager and self.selection_manager.has_selection():
            shape = self.selection_manager.get_selected_shape()
            if shape in self.shape_manager.shapes:
                self.shape_manager.shapes.remove(shape)
                self.selection_manager.clear_selection()
                return True
        return False

    def clear_canvas(self):
        if self.shape_manager:
            self.shape_manager.shapes.clear()
            if self.selection_manager: self.selection_manager.clear_selection()
            return True
        return False

    def get_current_color(self):
        return self.current_color

    def set_selected_shape(self, shape):
        """Legacy support for main.py."""
        pass
