class SelectionManager:
    def __init__(self, shape_manager, transform_manager=None):
        self.shape_manager = shape_manager
        self.transform_manager = transform_manager
        self.selected_shape = None

    def select(self, x, y):
        self.clear_selection()

        for shape in reversed(self.shape_manager.shapes):

            if not shape.vertices:
                continue

            if self.hit_test(shape, x, y):
                shape.selected = True
                self.selected_shape = shape

                if self.transform_manager:
                    self.transform_manager.set_target(shape)

                return shape

        return None

    def clear_selection(self):
        if self.selected_shape:
            self.selected_shape.selected = False
            self.selected_shape = None

        if self.transform_manager:
            self.transform_manager.set_target(None)

    def get_selected_shape(self):
        return self.selected_shape

    def has_selection(self):
        return self.selected_shape is not None

    def hit_test(self, shape, x, y):
        xs = [v[0] + shape.transform.tx for v in shape.vertices]
        ys = [v[1] + shape.transform.ty for v in shape.vertices]

        margin = 10

        return (
            min(xs) - margin <= x <= max(xs) + margin
            and
            min(ys) - margin <= y <= max(ys) + margin
        )