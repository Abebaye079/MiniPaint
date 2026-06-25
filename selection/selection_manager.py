import math
from shapes.shape import Tool
from transform.matrix import transform_point


def hit_test(shape, wx: float, wy: float, thresh: float = 0.8) -> bool:
    world_pts = [transform_point(shape, p[0], p[1]) for p in shape.pts]
    n    = len(world_pts)
    segs = n if shape.type == Tool.POLYGON else n - 1

    for i in range(segs):
        ax, ay = world_pts[i]
        bx, by = world_pts[(i + 1) % n]
        dx, dy = bx - ax, by - ay
        len2   = dx * dx + dy * dy
        if len2 > 1e-9:
            t = max(0.0, min(1.0, ((wx - ax) * dx + (wy - ay) * dy) / len2))
        else:
            t = 0.0
        cx2 = ax + t * dx - wx
        cy2 = ay + t * dy - wy
        if math.hypot(cx2, cy2) < thresh:
            return True
    return False


class SelectionManager:

    def __init__(self):
        self._selected: int = -1

    @property
    def selected(self) -> int:
        return self._selected

    def select(self, idx: int) -> None:
        self._selected = idx

    def deselect(self) -> None:
        self._selected = -1

    def clamp(self, total: int) -> None:
        if self._selected >= total:
            self._selected = -1

    def is_valid(self, total: int) -> bool:
        return 0 <= self._selected < total