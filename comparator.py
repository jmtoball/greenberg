from PIL import Image
from os import path
from difflib import SequenceMatcher
from operator import itemgetter, add, sub, mul, div
from math import sqrt

def area(box):
    x1, y1, x2, y2 = box
    return (x2 - x1) * (y2 - y1)

def img_box(image):
    return image.getbbox()

def color_diff(color1, color2):
    diff_vector = map(sub, color1, color2)
    diff_scalar = sqrt(sum(map(mul, diff_vector, diff_vector)))
    return diff_scalar/sqrt(255**2 * 3)

class Loader(object):

    @staticmethod
    def load(path):
        return Image.open(path)


class ImageOperation(object):

    def __init__(self, image, **options):
        self.image = image
        self.options = options

class Boxed(object):

    def box(self):
        return self.options.get('box') or img_box(self.image)

class ColorCountList(ImageOperation, Boxed):

    def get(self):
        box = self.box()
        return self.image.crop(box).getcolors(area(box))

class AverageColor(ImageOperation, Boxed):

    def get(self):
        box = self.box()
        colors = ColorCountList(self.image, box=box).get()
        color_count = area(box)
        total = (0.0, 0.0, 0.0)
        for (amount, color) in colors:
            weighted = map(mul, (amount,)*3, color)
            total = map(add, total, weighted)
        return map(div, total, (color_count,)*3)

class DominantColor(ImageOperation, Boxed):

    def get(self):
        colors = ColorCountList(self.image, box=self.box()).get()
        return max(colors, key=itemgetter(0))[1]


class Comparator(object):

    def __init__(self, path_one, path_two):
        self.path_one = path_one
        self.path_two = path_two

    def compare(self):
        pass

class ImageComparator(Comparator):

    def __init__(self, path_one, path_two):
        super(ImageComparator, self).__init__(path_one, path_two)
        self.image_one = Loader.load(self.path_one)
        self.image_two = Loader.load(self.path_two)

class FileNameComparator(Comparator):

    def compare(self):
        return SequenceMatcher(None,
            path.basename(self.path_one),
            path.basename(self.path_two)
        ).ratio()

class AverageColorComparator(ImageComparator):

    def compare(self):
        return 1.0 - color_diff(
            AverageColor(self.image_one).get(),
            AverageColor(self.image_two).get()
        )

class DominantColorComparator(ImageComparator):

    def compare(self):
        return 1.0 - color_diff(
            DominantColor(self.image_one).get(),
            DominantColor(self.image_two).get()
        )
