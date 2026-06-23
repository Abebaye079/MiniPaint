import math
import ctypes
from OpenGL.GL import *


def translation_matrix(tx, ty):
    """
    Build a 3x3 2D homogeneous translation matrix.

    | 1  0  tx |
    | 0  1  ty |
    | 0  0  1  |
    """
    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0,  1],
    ]


def rotation_matrix(angle_deg):
    """
    Build a 3x3 2D homogeneous rotation matrix (CCW positive).
    Note: Abebaye's viewport has y-down, so visually CW on screen.

    | cos  -sin  0 |
    | sin   cos  0 |
    |  0     0   1 |
    """
    angle_rad = math.radians(angle_deg)
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    return [
        [ c, -s, 0],
        [ s,  c, 0],
        [ 0,  0, 1],
    ]


def scale_matrix(sx, sy):
    """
    Build a 3x3 2D homogeneous scale matrix.

    | sx  0   0 |
    |  0  sy  0 |
    |  0  0   1 |
    """
    return [
        [sx,  0, 0],
        [ 0, sy, 0],
        [ 0,  0, 1],
    ]


def multiply_3x3(A, B):
    """
    Multiply two 3x3 matrices (list-of-rows format).
    Returns a new 3x3 matrix.
    """
    result = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[i][j] += A[i][k] * B[k][j]
    return result


def compose(tx, ty, angle_deg, sx, sy):
    """
    Compose a final TRS matrix in the correct order:
        M = Translation * Rotation * Scale

    OpenGL applies matrices right-to-left, so the vertex is:
        1. Scaled first
        2. Rotated around local origin
        3. Translated to world position

    This matches the standard per-shape transform pipeline.
    """
    T = translation_matrix(tx, ty)
    R = rotation_matrix(angle_deg)
    S = scale_matrix(sx, sy)

    # T * (R * S)
    RS = multiply_3x3(R, S)
    TRS = multiply_3x3(T, RS)
    return TRS


def to_opengl_matrix(m3x3):
    """
    Convert a 3x3 homogeneous 2D matrix into a 4x4 column-major
    flat float array suitable for glMultMatrixf().

    3x3:               4x4 (column-major for OpenGL):
    | m00 m01 m02 |    | m00  m10   0   0 |   <- col 0
    | m10 m11 m12 | -> | m01  m11   0   0 |   <- col 1
    | m20 m21 m22 |    |  0    0    1   0 |   <- col 2
                       | m02  m12   0   1 |   <- col 3

    OpenGL uses column-major order, so we fill by columns.
    The Z row/col is identity since this is a pure 2D transform.
    The translation sits in the 4th column (indices 12 and 13).
    """
    m = m3x3
    # fmt: off
    return (GLfloat * 16)(
        m[0][0], m[1][0], 0.0, 0.0,   # column 0
        m[0][1], m[1][1], 0.0, 0.0,   # column 1
        0.0,     0.0,     1.0, 0.0,   # column 2  (Z passthrough)
        m[0][2], m[1][2], 0.0, 1.0,   # column 3  (translation)
    )
    # fmt: on


def apply_matrix(tx, ty, angle_deg, sx, sy):
    """
    Convenience function: compose the TRS matrix and multiply it
    onto OpenGL's current MODELVIEW matrix using glMultMatrixf.

    Call this inside a glPushMatrix() / glPopMatrix() block.
    """
    trs = compose(tx, ty, angle_deg, sx, sy)
    gl_matrix = to_opengl_matrix(trs)
    glMultMatrixf(gl_matrix)
