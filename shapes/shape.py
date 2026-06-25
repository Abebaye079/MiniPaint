class Tool:
    LINE     = "LINE"
    POLYLINE = "POLYLINE"
    POLYGON  = "POLYGON"
    SELECT   = "SELECT"


class Shape:
    def __init__(self, stype: str, pts: list, color: tuple,
                 lw: float, filled: bool):
        self.type   = stype
        self.pts    = pts        
        self.color  = color
        self.lw     = lw
        self.filled = filled

        # Affine transform state 
        self.tx:    float = 0.0
        self.ty:    float = 0.0
        self.angle: float = 0.0   
        self.sx:    float = 1.0
        self.sy:    float = 1.0