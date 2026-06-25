from OpenGL.GL import glTranslatef, glRotatef, glScalef
from transform.matrix import centroid


def apply_transform(shape) -> None:
    cx, cy = centroid(shape.pts)

    glTranslatef(shape.tx, shape.ty, 0)
    glTranslatef(cx, cy, 0)
    glRotatef(shape.angle, 0, 0, 1)
    glScalef(shape.sx, shape.sy, 1)
    glTranslatef(-cx, -cy, 0)