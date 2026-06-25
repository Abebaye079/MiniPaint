from OpenGL.GL import (
    glBegin, glEnd, glVertex2f, glColor3f,
    glLineWidth, glRasterPos2f,
    glMatrixMode, glLoadIdentity, glPushMatrix, glPopMatrix,
    GL_LINES, GL_QUADS, GL_LINE_LOOP, GL_PROJECTION, GL_MODELVIEW,
)
from OpenGL.GLU import gluOrtho2D
from OpenGL.GLUT import (
    glutBitmapCharacter,
    GLUT_BITMAP_8_BY_13, GLUT_BITMAP_9_BY_15,
)

from shapes.shape import Tool
from core.constants import cfg, PALETTE, SIDEBAR

class UIManager:

    def __init__(self, state: dict, shape_mgr, selection_mgr):
        self._state     = state
        self._shapes    = shape_mgr
        self._selection = selection_mgr

    # Public entry points 
    def draw_sidebar(self):
        WIN_W = cfg["WIN_W"]
        WIN_H = cfg["WIN_H"]
        VP_W  = cfg["VP_W"]

        self._push_pixel_ortho(WIN_W, WIN_H)

        sx  = VP_W
        tx0 = sx + 10
        y   = WIN_H - 22

        # Background
        self._rect(sx, 0, SIDEBAR, WIN_H, (0.10, 0.10, 0.16))
        glColor3f(0.28, 0.28, 0.40)
        glBegin(GL_LINES); glVertex2f(sx, 0); glVertex2f(sx, WIN_H); glEnd()

        # Title
        self._text(tx0, y, "MINI PAINT", (0.40, 0.80, 1.00), GLUT_BITMAP_9_BY_15); y -= 6
        self._divider(sx, y); y -= 18

        # Tools
        self._text(tx0, y, "[ TOOLS ]", (0.65, 0.65, 0.65)); y -= 16
        for key, name, t in [('[L]', 'Line', Tool.LINE), ('[P]', 'Polyline', Tool.POLYLINE),
                               ('[G]', 'Polygon', Tool.POLYGON), ('[S]', 'Select', Tool.SELECT)]:
            active = self._state["tool"] == t
            self._rect(sx + 4, y - 2, SIDEBAR - 8, 15,
                       (0.18, 0.45, 0.80) if active else (0.06, 0.06, 0.10))
            self._text(tx0 + 2, y, f" {key} {name}",
                       (1, 1, 1) if active else (0.70, 0.70, 0.70))
            y -= 16

        y -= 4; self._divider(sx, y); y -= 16

        # Polygon options
        s = self._state
        self._text(tx0, y, "[ POLYGON OPTIONS ]",          (0.65, 0.65, 0.65)); y -= 16
        self._text(tx0, y, f" Sides: {s['poly_sides']}  (+/-)", (0.90, 0.90, 0.55)); y -= 16
        self._text(tx0, y,
                   " Fill: ON  [F]" if s["fill_polygon"] else " Fill: OFF [F]",
                   (0.40, 0.90, 0.40) if s["fill_polygon"] else (0.70, 0.70, 0.70)); y -= 16
        self._text(tx0, y, f" Width: {int(s['line_width'])}  [ / ]", (0.90, 0.90, 0.55)); y -= 16

        y -= 4; self._divider(sx, y); y -= 16

        # Colour palette
        self._text(tx0, y, "[ COLOUR  (0-9) ]", (0.65, 0.65, 0.65)); y -= 20
        cols, cw, ch, gap = 5, 22, 18, 5
        for i, col in enumerate(PALETTE):
            c, row = i % cols, i // cols
            px = sx + 10 + c * (cw + gap)
            py = y - row * (ch + gap)
            glColor3f(*col)
            glBegin(GL_QUADS)
            glVertex2f(px,      py - ch); glVertex2f(px + cw, py - ch)
            glVertex2f(px + cw, py     ); glVertex2f(px,      py     )
            glEnd()
            if i == s["color_idx"]:
                glColor3f(1, 1, 0); glLineWidth(2)
                glBegin(GL_LINE_LOOP)
                glVertex2f(px - 1,      py - ch - 1); glVertex2f(px + cw + 1, py - ch - 1)
                glVertex2f(px + cw + 1, py + 1     ); glVertex2f(px - 1,      py + 1     )
                glEnd()
        y -= 2 * (ch + gap) + 8

        self._divider(sx, y); y -= 16

        # Transform info
        self._text(tx0, y, "[ TRANSFORM ]", (0.65, 0.65, 0.65)); y -= 16
        sel = self._selection.selected
        if s["tool"] == Tool.SELECT and self._selection.is_valid(len(self._shapes)):
            sh = self._shapes[sel]
            for label in [" Translate: Arrows", " Rotate:    R / E",
                          " Scale uni: = / -",  " Scale X:   X / x", " Scale Y:   Y / y"]:
                self._text(tx0, y, label, (0.80, 0.80, 0.80)); y -= 14
            y -= 4
            self._text(tx0, y, f" tx={sh.tx:.1f}  ty={sh.ty:.1f}", (0.50, 1.00, 0.50)); y -= 14
            self._text(tx0, y, f" rot={sh.angle:.1f}deg",           (0.50, 1.00, 0.50)); y -= 14
            self._text(tx0, y, f" sx={sh.sx:.2f}  sy={sh.sy:.2f}", (0.50, 1.00, 0.50)); y -= 14
        else:
            self._text(tx0, y, " (select a shape)", (0.45, 0.45, 0.45)); y -= 14

        self._divider(sx, y); y -= 16

        # Edit shortcuts
        self._text(tx0, y, "[ EDIT ]", (0.65, 0.65, 0.65)); y -= 16
        for label in [" [Z] Undo", " [Del] Delete sel", " [C] Clear all",
                      " [Enter] End polyline", " [Esc] Cancel"]:
            self._text(tx0, y, label, (0.75, 0.75, 0.75)); y -= 14

        self._pop_pixel_ortho()

    def draw_status_bar(self):
        VP_W = cfg["VP_W"]
        VP_H = cfg["VP_H"]

        self._push_pixel_ortho(VP_W, VP_H)
        self._rect(0, 0, VP_W, 20, (0.0, 0.0, 0.05))
        mw = self._state["mouse_world"]
        status = (f"Tool: {self._state['tool']:<8}  |  "
                  f"World: ({mw[0]:.2f}, {mw[1]:.2f})  |  "
                  f"Shapes: {len(self._shapes)}")
        self._text(6, 5, status, (0.50, 0.90, 0.50))
        self._pop_pixel_ortho()

    # Private draw helpers 
    def _text(self, x, y, text, color=(1, 1, 1), font=GLUT_BITMAP_8_BY_13):
        glColor3f(*color)
        glRasterPos2f(x, y)
        for ch in text:
            glutBitmapCharacter(font, ord(ch))

    def _rect(self, x, y, w, h, color):
        glColor3f(*color)
        glBegin(GL_QUADS)
        glVertex2f(x,     y    ); glVertex2f(x + w, y    )
        glVertex2f(x + w, y + h); glVertex2f(x,     y + h)
        glEnd()

    def _divider(self, sx, y):
        glColor3f(0.28, 0.28, 0.40)
        glBegin(GL_LINES)
        glVertex2f(sx + 4, y); glVertex2f(sx + SIDEBAR - 4, y)
        glEnd()

    def _push_pixel_ortho(self, w, h):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix(); glLoadIdentity()
        gluOrtho2D(0, w, 0, h)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix(); glLoadIdentity()

    def _pop_pixel_ortho(self):
        glPopMatrix()
        glMatrixMode(GL_PROJECTION); glPopMatrix()
        glMatrixMode(GL_MODELVIEW)