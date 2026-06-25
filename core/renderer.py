import math

from OpenGL.GL import (
    glBegin, glEnd, glVertex2f, glColor3f, glColor4f,
    glLineWidth, glMatrixMode, glLoadIdentity, glViewport,
    glClear, glClearColor, glEnable, glDisable, glLineStipple,
    glPushMatrix, glPopMatrix,
    GL_LINES, GL_LINE_STRIP, GL_LINE_LOOP, GL_POLYGON,
    GL_MODELVIEW, GL_PROJECTION, GL_COLOR_BUFFER_BIT, GL_LINE_STIPPLE,
)
from OpenGL.GLU import gluOrtho2D
from OpenGL.GLUT import glutSwapBuffers

from shapes.shape import Tool
from shapes.polygon import regular_polygon_vertices
from transform.transform import apply_transform
from core.constants import cfg, PALETTE, WX_MIN, WX_MAX, WY_MIN, WY_MAX, VP_X, VP_Y, SIDEBAR


class Renderer:

    def __init__(self, state: dict, shape_mgr, selection_mgr, ui_mgr):
        self._state     = state
        self._shapes    = shape_mgr
        self._selection = selection_mgr
        self._ui        = ui_mgr

    def display(self):
        VP_W  = cfg["VP_W"]
        VP_H  = cfg["VP_H"]
        WIN_W = cfg["WIN_W"]
        WIN_H = cfg["WIN_H"]

        glClearColor(0.05, 0.05, 0.08, 1)
        glClear(GL_COLOR_BUFFER_BIT)

        # Drawing viewport
        glViewport(VP_X, VP_Y, VP_W, VP_H)
        glMatrixMode(GL_PROJECTION); glLoadIdentity()
        gluOrtho2D(WX_MIN, WX_MAX, WY_MIN, WY_MAX)
        glMatrixMode(GL_MODELVIEW); glLoadIdentity()

        self._draw_grid()

        for i, sh in enumerate(self._shapes.shapes):
            self._draw_shape(sh, highlight=(i == self._selection.selected))

        self._draw_preview()
        self._ui.draw_status_bar()

        # Full-window sidebar
        glViewport(0, 0, WIN_W, WIN_H)
        self._ui.draw_sidebar()

        glutSwapBuffers()

    # Grid & axes
    def _draw_grid(self):
        glLineWidth(1.0)
        glColor3f(0.13, 0.13, 0.20)
        glBegin(GL_LINES)
        for gx in range(int(WX_MIN), int(WX_MAX) + 1):
            glVertex2f(gx, WY_MIN); glVertex2f(gx, WY_MAX)
        for gy in range(int(WY_MIN), int(WY_MAX) + 1):
            glVertex2f(WX_MIN, gy); glVertex2f(WX_MAX, gy)
        glEnd()
        glColor3f(0.22, 0.22, 0.33)
        glBegin(GL_LINES)
        glVertex2f(0, WY_MIN); glVertex2f(0, WY_MAX)
        glVertex2f(WX_MIN, 0); glVertex2f(WX_MAX, 0)
        glEnd()

    # Shape drawing
    def _draw_shape(self, shape, highlight=False):
        glPushMatrix()
        apply_transform(shape)

        if highlight:
            glLineWidth(shape.lw + 3)
            glColor3f(1.0, 0.9, 0.0)
            mode = GL_LINE_LOOP if shape.type == Tool.POLYGON else GL_LINE_STRIP
            glBegin(mode)
            for p in shape.pts: glVertex2f(*p)
            glEnd()

        glLineWidth(shape.lw)
        glColor3f(*shape.color)

        if shape.type == Tool.LINE:
            glBegin(GL_LINES)
            for p in shape.pts: glVertex2f(*p)
            glEnd()

        elif shape.type == Tool.POLYLINE:
            glBegin(GL_LINE_STRIP)
            for p in shape.pts: glVertex2f(*p)
            glEnd()

        elif shape.type == Tool.POLYGON:
            if shape.filled:
                glBegin(GL_POLYGON)
                for p in shape.pts: glVertex2f(*p)
                glEnd()
                r, g, b = shape.color
                glColor3f(r * 0.6, g * 0.6, b * 0.6)
            glBegin(GL_LINE_LOOP)
            for p in shape.pts: glVertex2f(*p)
            glEnd()

        glPopMatrix()

    # Rubber-band preview
    def _draw_preview(self):
        s = self._state
        if not s["drawing"]:
            return

        glEnable(GL_LINE_STIPPLE)
        glLineStipple(1, 0xAAAA)
        glLineWidth(s["line_width"])
        glColor3f(*PALETTE[s["color_idx"]])

        mw  = s["mouse_world"]
        pts = s["pending_pts"]
        t   = s["pending_type"]

        if t == Tool.LINE and pts:
            glBegin(GL_LINES)
            glVertex2f(*pts[0]); glVertex2f(*mw)
            glEnd()

        elif t == Tool.POLYLINE and pts:
            glBegin(GL_LINE_STRIP)
            for p in pts: glVertex2f(*p)
            glVertex2f(*mw)
            glEnd()

        elif t == Tool.POLYGON and pts:
            cx, cy = pts[0]
            r = math.hypot(mw[0] - cx, mw[1] - cy)
            if r > 0.05:
                verts = regular_polygon_vertices(cx, cy, r, s["poly_sides"])
                if s["fill_polygon"]:
                    glDisable(GL_LINE_STIPPLE)
                    glColor4f(*PALETTE[s["color_idx"]], 0.25)
                    glBegin(GL_POLYGON)
                    for p in verts: glVertex2f(*p)
                    glEnd()
                    glEnable(GL_LINE_STIPPLE)
                    glColor3f(*PALETTE[s["color_idx"]])
                glBegin(GL_LINE_LOOP)
                for p in verts: glVertex2f(*p)
                glEnd()

        glDisable(GL_LINE_STIPPLE)