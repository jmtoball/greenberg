from greenberg.comparators import ImageComparator
from greenberg import Color

class ColorComparator(ImageComparator):

    def __init__(self, path_one, path_two, color_operation):
        super(ColorComparator, self).__init__(path_one, path_two)
        self.color_operation = color_operation

    def compare(self):
        return 1.0 - Color.diff(
            self.color_operation(self.image_one).get(),
            self.color_operation(self.image_two).get()
        )
