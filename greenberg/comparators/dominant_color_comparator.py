from greenberg.comparators import ImageComparator
from greenberg.comparators import ColorComparator
from greenberg.operations import DominantColor

class DominantColorComparator(ImageComparator, ColorComparator):

    def compare(self):
        return 1.0 - self.color_diff(
            DominantColor(self.image_one).get(),
            DominantColor(self.image_two).get()
        )
