class BoxedOperation(object):

    def box(self):
        return self.options.get('box') or ((0, 0) + self.image.size)

    def area(self):
        x1, y1, x2, y2 = self.box()
        return (x2 - x1) * (y2 - y1)
