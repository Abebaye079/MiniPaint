import sys

from OpenGL.GL import (
    glEnable, glBlendFunc, glHint,
    GL_BLEND, GL_LINE_SMOOTH, GL_LINE_SMOOTH_HINT,
    GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_NICEST,
)
from OpenGL.GLUT import (
    glutInit, glutInitDisplayMode, glutInitWindowSize, glutInitWindowPosition,
    glutCreateWindow, glutDisplayFunc, glutReshapeFunc,
    glutMouseFunc, glutMotionFunc, glutPassiveMotionFunc,
    glutKeyboardFunc, glutSpecialFunc, glutMainLoop, glutPostRedisplay,
    GLUT_DOUBLE, GLUT_RGB,
)

from core.constants  import cfg, SIDEBAR
from shapes.shape    import Tool
from shapes.shape_manager    import ShapeManager
from selection.selection_manager import SelectionManager
from transform.transform_manager import TransformManager
from input.mouse_handler    import MouseHandler
from input.keyboard_handler import KeyboardHandler
from ui.ui_manager   import UIManager
from core.renderer   import Renderer


#  APPLICATION STATE
state = {
    "tool"         : Tool.LINE,
    "color_idx"    : 0,
    "line_width"   : 2.0,
    "poly_sides"   : 5,
    "fill_polygon" : False,
    "drawing"      : False,
    "pending_pts"  : [],
    "pending_type" : None,
    "mouse_world"  : (0.0, 0.0),
}


#  MANAGER OBJECTS
shape_mgr     = ShapeManager()
selection_mgr = SelectionManager()
ui_mgr        = UIManager(state, shape_mgr, selection_mgr)
renderer      = Renderer(state, shape_mgr, selection_mgr, ui_mgr)
mouse_handler = MouseHandler(state, shape_mgr, selection_mgr)
kb_handler    = KeyboardHandler(state, shape_mgr, selection_mgr)


#  GLUT CALLBACK WRAPPERS
def display_cb():
    renderer.display()

def reshape_cb(w, h):
    cfg["WIN_W"] = w
    cfg["WIN_H"] = h
    cfg["VP_W"]  = w - SIDEBAR
    cfg["VP_H"]  = h
    glutPostRedisplay()

def mouse_cb(button, mstate, sx, sy):
    mouse_handler.on_click(button, mstate, sx, sy)

def motion_cb(sx, sy):
    mouse_handler.on_motion(sx, sy)

def passive_cb(sx, sy):
    mouse_handler.on_passive(sx, sy)

def keyboard_cb(key, x, y):
    kb_handler.on_key(key, x, y)

def special_cb(key, x, y):
    kb_handler.on_special(key, x, y)


#  MAIN
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(cfg["WIN_W"], cfg["WIN_H"])
    glutInitWindowPosition(100, 80)
    glutCreateWindow(b"Mini Paint -- CG Capstone (Python/OpenGL)")

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

    glutDisplayFunc(display_cb)
    glutReshapeFunc(reshape_cb)
    glutMouseFunc(mouse_cb)
    glutMotionFunc(motion_cb)
    glutPassiveMotionFunc(passive_cb)
    glutKeyboardFunc(keyboard_cb)
    glutSpecialFunc(special_cb)

    glutMainLoop()


if __name__ == "__main__":
    main()