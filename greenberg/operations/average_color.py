from greenberg.operations import ImageOperation, BoxedOperation, ColorCountList
from greenberg import Color

class AverageColor(ImageOperation, BoxedOperation):

    def get(self):
        colors = ColorCountList(self.image, box=self.box()).get()
        return Color.avg_weighted(colors)
