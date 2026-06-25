import math

from OpenGL.GLUT import (
    glutPostRedisplay,
    GLUT_LEFT_BUTTON, GLUT_DOWN, GLUT_UP,
)

from shapes.shape import Tool
from shapes.polygon import regular_polygon_vertices
from core.viewport import screen_to_world, in_viewport
from core.constants import PALETTE, cfg, SIDEBAR


class MouseHandler:

    def __init__(self, state: dict, shape_mgr, selection_mgr):
        self._state    = state
        self._shapes   = shape_mgr
        self._selection = selection_mgr

    #  Public GLUT callbacks
    def on_click(self, button, mstate, sx, sy):
        if button != GLUT_LEFT_BUTTON:
            return

        if not in_viewport(sx):
            if mstate == GLUT_DOWN:
                self._try_pick_colour(sx, sy)
            glutPostRedisplay()
            return

        w    = screen_to_world(sx, sy)
        self._state["mouse_world"] = w
        tool = self._state["tool"]

        if mstate == GLUT_DOWN:
            self._handle_down(tool, w)
        elif mstate == GLUT_UP:
            self._handle_up(tool, w)

        glutPostRedisplay()

    def on_motion(self, sx, sy):
        self._state["mouse_world"] = screen_to_world(sx, sy)
        glutPostRedisplay()

    def on_passive(self, sx, sy):
        self._state["mouse_world"] = screen_to_world(sx, sy)
        glutPostRedisplay()

    # Internal helpers 
    def _handle_down(self, tool, w):
        s = self._state

        if tool == Tool.SELECT:
            idx = self._shapes.find_shape_at(w[0], w[1])
            self._selection.select(idx)

        elif tool == Tool.LINE:
            s["drawing"]      = True
            s["pending_type"] = Tool.LINE
            s["pending_pts"]  = [w]

        elif tool == Tool.POLYLINE:
            if not s["drawing"]:
                s["drawing"]      = True
                s["pending_type"] = Tool.POLYLINE
                s["pending_pts"]  = [w]
            else:
                s["pending_pts"].append(w)

        elif tool == Tool.POLYGON:
            s["drawing"]      = True
            s["pending_type"] = Tool.POLYGON
            s["pending_pts"]  = [w]

    def _handle_up(self, tool, w):
        s = self._state

        if tool == Tool.LINE and s["drawing"]:
            p1 = s["pending_pts"][0]
            self._shapes.commit_line(
                p1, w,
                PALETTE[s["color_idx"]], s["line_width"], s["fill_polygon"]
            )
            s["drawing"] = False

        elif tool == Tool.POLYGON and s["drawing"]:
            cx, cy = s["pending_pts"][0]
            r = math.hypot(w[0] - cx, w[1] - cy)
            if r > 0.1:
                self._shapes.commit_polygon(
                    cx, cy, r, s["poly_sides"],
                    PALETTE[s["color_idx"]], s["line_width"], s["fill_polygon"]
                )
            s["drawing"] = False

    def _try_pick_colour(self, sx, sy):
        VP_W  = cfg["VP_W"]
        WIN_H = cfg["WIN_H"]
        bx    = VP_W + 10
        oy    = WIN_H - sy          # flip y (GLUT → ortho)
        cols, cw, ch, gap = 5, 22, 18, 5
        pal_top = WIN_H - 280
        for i in range(len(PALETTE)):
            c, r = i % cols, i // cols
            px = bx + c * (cw + gap)
            py = pal_top - r * (ch + gap)
            if px <= sx < px + cw and py - ch <= oy <= py:
                self._state["color_idx"] = i
                return