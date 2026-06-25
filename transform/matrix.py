import math


def centroid(pts: list) -> tuple[float, float]:
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    return (cx, cy)


def transform_point(shape, px: float, py: float) -> tuple[float, float]:
    cx, cy = centroid(shape.pts)

    # 1. Scale around centroid
    px = cx + (px - cx) * shape.sx
    py = cy + (py - cy) * shape.sy

    # 2. Rotate around centroid
    rad = math.radians(shape.angle)
    c, s = math.cos(rad), math.sin(rad)
    rx = cx + (px - cx) * c - (py - cy) * s
    ry = cy + (px - cx) * s + (py - cy) * c

    # 3. Translate
    return (rx + shape.tx, ry + shape.ty)