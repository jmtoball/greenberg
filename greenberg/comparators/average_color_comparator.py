from greenberg.comparators import ImageComparator, ColorComparator
from greenberg.operations import AverageColor

class AverageColorComparator(ImageComparator, ColorComparator):

    def compare(self):
        return 1.0 - self.color_diff(
            AverageColor(self.image_one).get(),
            AverageColor(self.image_two).get()
        )
