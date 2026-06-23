class TransformManager:
    """
    Controls real-time transformations on whichever shape is currently selected.

    Sits between the keyboard handler (Tsion) and the Transform data on each
    shape. The selection manager (Nanat) calls set_target() whenever the user
    clicks a shape. Tsion's keyboard handler calls the action methods below.

    Design rule: NEVER touch shape.vertices. Only shape.transform is modified.
    """

    # How much each keypress moves / rotates / scales by default.
    # Tsion can override these if she wants fine/coarse control modes.
    TRANSLATE_STEP = 5.0       # pixels per keypress
    ROTATE_STEP    = 5.0       # degrees per keypress
    SCALE_STEP     = 1.05      # 5% grow / shrink per keypress
    SCALE_STEP_INV = 1 / 1.05  # inverse for shrink

    def __init__(self):
        self._target = None    # the currently selected Shape (or None)

    # ------------------------------------------------------------------
    # Target management  (called by Nanat's SelectionManager)
    # ------------------------------------------------------------------

    def set_target(self, shape):
        """Point the manager at a newly selected shape. Pass None to deselect."""
        self._target = shape

    def get_target(self):
        return self._target

    def has_target(self):
        return self._target is not None

    # ------------------------------------------------------------------
    # Translation  (arrow keys or WASD — Tsion decides)
    # ------------------------------------------------------------------

    def move_left(self, step=None):
        self._apply(lambda t: t.translate(-(step or self.TRANSLATE_STEP), 0))

    def move_right(self, step=None):
        self._apply(lambda t: t.translate(+(step or self.TRANSLATE_STEP), 0))

    def move_up(self, step=None):
        # y increases downward in Abebaye's viewport, so "up" means negative dy
        self._apply(lambda t: t.translate(0, -(step or self.TRANSLATE_STEP)))

    def move_down(self, step=None):
        self._apply(lambda t: t.translate(0, +(step or self.TRANSLATE_STEP)))

    # ------------------------------------------------------------------
    # Rotation  ([ and ] keys — Tsion decides)
    # ------------------------------------------------------------------

    def rotate_ccw(self, step=None):
        """Rotate counter-clockwise (negative angle in y-down viewport)."""
        self._apply(lambda t: t.rotate(-(step or self.ROTATE_STEP)))

    def rotate_cw(self, step=None):
        """Rotate clockwise."""
        self._apply(lambda t: t.rotate(+(step or self.ROTATE_STEP)))

    # ------------------------------------------------------------------
    # Scaling  (+ / - keys — Tsion decides)
    # ------------------------------------------------------------------

    def scale_up(self, factor=None):
        """Grow the shape uniformly."""
        f = factor or self.SCALE_STEP
        self._apply(lambda t: t.scale(f, f))

    def scale_down(self, factor=None):
        """Shrink the shape uniformly."""
        f = factor or self.SCALE_STEP_INV
        self._apply(lambda t: t.scale(f, f))

    def scale_x_up(self, factor=None):
        f = factor or self.SCALE_STEP
        self._apply(lambda t: t.scale(f, 1.0))

    def scale_x_down(self, factor=None):
        f = factor or self.SCALE_STEP_INV
        self._apply(lambda t: t.scale(f, 1.0))

    def scale_y_up(self, factor=None):
        f = factor or self.SCALE_STEP
        self._apply(lambda t: t.scale(1.0, f))

    def scale_y_down(self, factor=None):
        f = factor or self.SCALE_STEP_INV
        self._apply(lambda t: t.scale(1.0, f))

    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------

    def reset_transform(self):
        """Snap the selected shape back to its original position/size/angle."""
        self._apply(lambda t: t.reset())

    # ------------------------------------------------------------------
    # Internal helper
    # ------------------------------------------------------------------

    def _apply(self, fn):
        """
        Run fn(transform) only if a target is selected.
        Silently does nothing otherwise so Tsion doesn't need to guard calls.
        """
        if self._target is not None:
            fn(self._target.transform)

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    def __repr__(self):
        if self._target is None:
            return "TransformManager(no target)"
        return f"TransformManager(target={self._target}, {self._target.transform})"
