import math
from shapes.shape import Shape, Tool


def regular_polygon_vertices(cx: float, cy: float,
                              r: float, n: int) -> list:
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def create_polygon(cx: float, cy: float, r: float, n: int,
                   color: tuple, lw: float, filled: bool) -> Shape:
    verts = regular_polygon_vertices(cx, cy, r, n)
    return Shape(Tool.POLYGON, verts, color, lw, filled)