from OpenGL.GLUT import (
    glutPostRedisplay,
    GLUT_KEY_LEFT, GLUT_KEY_RIGHT, GLUT_KEY_UP, GLUT_KEY_DOWN,
)

from shapes.shape import Tool
from core.constants import PALETTE
from transform.transform_manager import TransformManager


class KeyboardHandler:

    def __init__(self, state: dict, shape_mgr, selection_mgr):
        self._state     = state
        self._shapes    = shape_mgr
        self._selection = selection_mgr
        self._tm        = TransformManager()

    #  Public GLUT callbacks 
    def on_key(self, key, x, y):
        key  = key.decode("utf-8", errors="ignore") if isinstance(key, bytes) else key
        s    = self._state
        sel  = self._selection.selected
        tool = s["tool"]

        # Tool switching
        if   key in ('l', 'L'): self._switch_tool(Tool.LINE)
        elif key in ('p', 'P'): self._switch_tool(Tool.POLYLINE)
        elif key in ('g', 'G'): self._switch_tool(Tool.POLYGON)
        elif key in ('s', 'S'): self._switch_tool(Tool.SELECT)

        # Polygon sides / uniform scale
        elif key == '+':
            s["poly_sides"] = min(20, s["poly_sides"] + 1)
        elif key == '-':
            if tool == Tool.SELECT and self._selection.is_valid(len(self._shapes)):
                self._tm.scale_down(self._shapes[sel])
            else:
                s["poly_sides"] = max(3, s["poly_sides"] - 1)
        elif key == '=':
            if tool == Tool.SELECT and self._selection.is_valid(len(self._shapes)):
                self._tm.scale_up(self._shapes[sel])
            else:
                s["poly_sides"] = min(20, s["poly_sides"] + 1)

        # Fill / line width
        elif key in ('f', 'F'): s["fill_polygon"] = not s["fill_polygon"]
        elif key == '[': s["line_width"] = max(1.0,  s["line_width"] - 1)
        elif key == ']': s["line_width"] = min(10.0, s["line_width"] + 1)

        # Colour shortcuts 0-9
        elif key in "0123456789":
            s["color_idx"] = int(key)

        # Rotate (Select mode)
        elif key in ('r', 'R') and self._selection.is_valid(len(self._shapes)):
            self._tm.rotate_ccw(self._shapes[sel])
        elif key in ('e', 'E') and self._selection.is_valid(len(self._shapes)):
            self._tm.rotate_cw(self._shapes[sel])

        # Non-uniform scale
        elif key == 'X' and self._selection.is_valid(len(self._shapes)):
            self._tm.scale_x_up(self._shapes[sel])
        elif key == 'x' and self._selection.is_valid(len(self._shapes)):
            self._tm.scale_x_down(self._shapes[sel])
        elif key == 'Y' and self._selection.is_valid(len(self._shapes)):
            self._tm.scale_y_up(self._shapes[sel])
        elif key == 'y' and self._selection.is_valid(len(self._shapes)):
            self._tm.scale_y_down(self._shapes[sel])

        # Finish polyline (Enter)
        elif key == '\r':
            if tool == Tool.POLYLINE and s["drawing"] and len(s["pending_pts"]) >= 2:
                self._shapes.commit_polyline(
                    s["pending_pts"],
                    PALETTE[s["color_idx"]], s["line_width"], s["fill_polygon"]
                )
                s["drawing"] = False

        # Undo (Z)
        elif key in ('z', 'Z'):
            if not s["drawing"]:
                self._shapes.undo()
                self._selection.clamp(len(self._shapes))
            elif tool == Tool.POLYLINE:
                if s["pending_pts"]:
                    s["pending_pts"].pop()
                if not s["pending_pts"]:
                    s["drawing"] = False

        # Delete selected (Del)
        elif key == '\x7f':
            if self._selection.is_valid(len(self._shapes)):
                self._shapes.delete(self._selection.selected)
                self._selection.deselect()

        # Clear canvas (C)
        elif key in ('c', 'C'):
            self._shapes.clear()
            self._selection.deselect()
            s["drawing"] = False

        # Cancel (Esc)
        elif key == '\x1b':
            s["drawing"]     = False
            s["pending_pts"] = []

        glutPostRedisplay()

    def on_special(self, key, x, y):
        sel = self._selection.selected
        if self._state["tool"] != Tool.SELECT or not self._selection.is_valid(len(self._shapes)):
            return
        sh = self._shapes[sel]
        if   key == GLUT_KEY_LEFT:  self._tm.move_left(sh)
        elif key == GLUT_KEY_RIGHT: self._tm.move_right(sh)
        elif key == GLUT_KEY_UP:    self._tm.move_up(sh)
        elif key == GLUT_KEY_DOWN:  self._tm.move_down(sh)
        glutPostRedisplay()

    #  Helpers 
    def _switch_tool(self, tool):
        self._state["tool"]    = tool
        self._state["drawing"] = False