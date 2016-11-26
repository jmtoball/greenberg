from greenberg import Loader
from greenberg.comparators import Comparator

class ImageComparator(Comparator):

    def __init__(self, path_one, path_two):
        super(ImageComparator, self).__init__(path_one, path_two)
        self.image_one = Loader.load(self.path_one)
        self.image_two = Loader.load(self.path_two)
