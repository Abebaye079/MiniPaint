class ShapeManager:
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape):
        self.shapes.append(shape)

    def remove_shape(self, shape):
        if shape in self.shapes:
            self.shapes.remove(shape)

    def clear(self):
        self.shapes.clear()

    def draw_all(self):
        for shape in self.shapes:
            shape.draw()
