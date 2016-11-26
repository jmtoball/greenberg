from greenberg.operations import ImageOperation, BoxedOperation, ColorCountList
from operator import add, mul, div

class AverageColor(ImageOperation, BoxedOperation):

    def get(self):
        colors = ColorCountList(self.image, box=self.box()).get()
        color_count = self.area()
        total = (0.0, 0.0, 0.0)
        for (amount, color) in colors:
            weighted = map(mul, (amount,)*3, color)
            total = map(add, total, weighted)
        return map(div, total, (color_count,)*3)
