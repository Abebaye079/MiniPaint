from shapes.shape import Shape, Tool
from core.constants import PALETTE

def create_line(p1: tuple, p2: tuple, color: tuple,
                lw: float, filled: bool = False) -> Shape:
    return Shape(Tool.LINE, [p1, p2], color, lw, filled)