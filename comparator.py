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

class ColorCountList(object):

    @staticmethod
    def of(image, box):
        return image.crop(box).getcolors(area(box))

class AverageColor(object):

    @staticmethod
    def of(image, box):
        colors = ColorCountList.of(image, box)
        color_count = area(box)
        total = (0.0, 0.0, 0.0)
        for (amount, color) in colors:
            weighted = map(mul, (amount,)*3, color)
            total = map(add, total, weighted)
        return map(div, total, (color_count,)*3)

class DominantColor(object):

    @staticmethod
    def of(image, box):
        colors = ColorCountList.of(image, box)
        return max(colors, key=itemgetter(0))[1]

class Comparator(object):

    def compare(self, path_one, path_two):
        pass

class FileNameComparator(Comparator):

    def compare(self, path_one, path_two):
        name_one = path.basename(path_one)
        name_two = path.basename(path_two)
        return SequenceMatcher(None, name_one, name_two).ratio()

class AverageColorComparator(Comparator):

    def compare(self, path_one, path_two):
        image_one = Loader.load(path_one)
        image_two = Loader.load(path_two)
        color_one = AverageColor.of(image_one, img_box(image_one))
        color_two = AverageColor.of(image_two, img_box(image_two))
        return 1.0 - color_diff(color_one, color_two)

class DominantColorComparator(Comparator):

    def compare(self, path_one, path_two):
        image_one = Loader.load(path_one)
        image_two = Loader.load(path_two)
        color_one = DominantColor.of(image_one, img_box(image_one))
        color_two = DominantColor.of(image_two, img_box(image_two))
        return 1.0 - color_diff(color_one, color_two)
