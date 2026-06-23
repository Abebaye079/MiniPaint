from transform.matrix import compose, to_opengl_matrix, apply_matrix


class Transform:
    """
    Stores all transformation state for a single shape.
    No vertices are ever modified — this data is read at draw time.

    Attributes:
        tx, ty      : translation in world (screen) coordinates
        rotation    : angle in degrees (CCW positive in math; visually CW
                      because Abebaye's viewport has y increasing downward)
        sx, sy      : scale factors (1.0 = original size)
    """

    def __init__(self):
        self.tx = 0.0
        self.ty = 0.0
        self.rotation = 0.0
        self.sx = 1.0
        self.sy = 1.0

    # ------------------------------------------------------------------
    # Matrix access
    # ------------------------------------------------------------------

    def get_matrix(self):
       
        return compose(self.tx, self.ty, self.rotation, self.sx, self.sy)

    def get_opengl_matrix(self):
        """
        Return a 4x4 column-major GLfloat array ready for glMultMatrixf().
        """
        return to_opengl_matrix(self.get_matrix())

    def apply(self):
        """
        Multiply this transform onto OpenGL's current MODELVIEW matrix.
        Must be called between glPushMatrix() and glPopMatrix().

        This is what shape.py's apply_opengl_transforms() calls.
        """
        apply_matrix(self.tx, self.ty, self.rotation, self.sx, self.sy)

    # ------------------------------------------------------------------
    # Convenience mutators (used by TransformManager)
    # ------------------------------------------------------------------

    def translate(self, dx, dy):
        """Shift the shape by (dx, dy) in screen coordinates."""
        self.tx += dx
        self.ty += dy

    def rotate(self, d_angle):
        """Add d_angle degrees to the current rotation. Wraps at 360."""
        self.rotation = (self.rotation + d_angle) % 360.0

    def scale(self, dsx, dsy):
        """
        Multiply current scale factors.
        dsx=1.1 makes the shape 10% wider; dsx=0.9 shrinks it 10%.
        Clamped to 0.01 so shapes can't collapse to zero.
        """
        self.sx = max(0.01, self.sx * dsx)
        self.sy = max(0.01, self.sy * dsy)

    def reset(self):
        """Return all transform values to their defaults."""
        self.tx = 0.0
        self.ty = 0.0
        self.rotation = 0.0
        self.sx = 1.0
        self.sy = 1.0

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self):
        return (
            f"Transform(tx={self.tx:.1f}, ty={self.ty:.1f}, "
            f"rotation={self.rotation:.1f}°, "
            f"sx={self.sx:.2f}, sy={self.sy:.2f})"
        )
