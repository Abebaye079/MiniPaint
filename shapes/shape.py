from transform.transform import Transform

class Shape:
    def __init__(self, color=(1, 0, 0)):
        self.vertices = []
        self.color = color
        self.transform = Transform()  # Stores tx, ty, rotation, sx, sy
        self.selected = False

    def draw(self):
        raise NotImplementedError("Subclasses must implement draw()")

    def apply_opengl_transforms(self):
        """
        Israel's Transformation Pipeline.
        Applies transformations using standard matrix multiplication order:
        Translation -> Rotation -> Scale
        """
        from OpenGL.GL import glTranslatef, glRotatef, glScalef
        
        # 1. Move the shape's coordinate space
        glTranslatef(self.transform.tx, self.transform.ty, 0.0)
        
        # 2. Rotate around the Z-axis (2D rotation)
        glRotatef(self.transform.rotation, 0.0, 0.0, 1.0)
        
        # 3. Scale the coordinate space
        glScalef(self.transform.sx, self.transform.sy, 1.0)
