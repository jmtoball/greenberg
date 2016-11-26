from greenberg.operations import ImageOperation, BoxedOperation, ColorCountList
from operator import itemgetter

class DominantColor(ImageOperation, BoxedOperation):

    def get(self):
        colors = ColorCountList(self.image, box=self.box()).get()
        return max(colors, key=itemgetter(0))[1]
