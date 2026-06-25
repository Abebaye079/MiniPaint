from shapes.shape import Shape, Tool

def create_polyline(pts: list, color: tuple,
                    lw: float, filled: bool = False) -> Shape:
    return Shape(Tool.POLYLINE, list(pts), color, lw, filled)