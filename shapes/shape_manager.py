import math

from shapes.shape import Shape, Tool
from shapes.line import create_line
from shapes.polyline import create_polyline
from shapes.polygon import create_polygon
from core.constants import PALETTE


class ShapeManager:
  
    def __init__(self):
        self._shapes: list[Shape] = []

    # Read access 
    @property
    def shapes(self) -> list[Shape]:
        return self._shapes

    def __len__(self) -> int:
        return len(self._shapes)

    def __getitem__(self, idx):
        return self._shapes[idx]

    # Mutations 
    def commit_line(self, p1, p2, color, lw, filled=False):
        self._shapes.append(create_line(p1, p2, color, lw, filled))

    def commit_polyline(self, pts, color, lw, filled=False):
        self._shapes.append(create_polyline(pts, color, lw, filled))

    def commit_polygon(self, cx, cy, r, n, color, lw, filled):
        self._shapes.append(create_polygon(cx, cy, r, n, color, lw, filled))

    def undo(self) -> bool:
        if self._shapes:
            self._shapes.pop()
            return True
        return False

    def delete(self, idx: int) -> bool:
        if 0 <= idx < len(self._shapes):
            self._shapes.pop(idx)
            return True
        return False

    def clear(self):
        self._shapes.clear()

    # Hit testing 
    def find_shape_at(self, wx: float, wy: float,
                      thresh: float = 0.8) -> int:
    
        from selection.selection_manager import hit_test   # avoid circular import
        for i in range(len(self._shapes) - 1, -1, -1):
            if hit_test(self._shapes[i], wx, wy, thresh):
                return i
        return -1