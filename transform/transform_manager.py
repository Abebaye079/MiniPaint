from core.constants import TSTEP, RSTEP, SSTEP

class TransformManager:
  
    # Translation 
    @staticmethod
    def translate(shape, dx: float, dy: float) -> None:
        shape.tx += dx
        shape.ty += dy

    @staticmethod
    def move_left(shape):  TransformManager.translate(shape, -TSTEP,  0)
    @staticmethod
    def move_right(shape): TransformManager.translate(shape,  TSTEP,  0)
    @staticmethod
    def move_up(shape):    TransformManager.translate(shape,  0,  TSTEP)
    @staticmethod
    def move_down(shape):  TransformManager.translate(shape,  0, -TSTEP)

    # Rotation 
    @staticmethod
    def rotate_cw(shape):  shape.angle -= RSTEP
    @staticmethod
    def rotate_ccw(shape): shape.angle += RSTEP

    # Uniform scale 
    @staticmethod
    def scale_up(shape):
        shape.sx *= (1 + SSTEP)
        shape.sy *= (1 + SSTEP)

    @staticmethod
    def scale_down(shape):
        shape.sx = max(0.05, shape.sx * (1 - SSTEP))
        shape.sy = max(0.05, shape.sy * (1 - SSTEP))

    # Non-uniform scale 
    @staticmethod
    def scale_x_up(shape):   shape.sx *= (1 + SSTEP)
    @staticmethod
    def scale_x_down(shape): shape.sx = max(0.05, shape.sx * (1 - SSTEP))
    @staticmethod
    def scale_y_up(shape):   shape.sy *= (1 + SSTEP)
    @staticmethod
    def scale_y_down(shape): shape.sy = max(0.05, shape.sy * (1 - SSTEP))