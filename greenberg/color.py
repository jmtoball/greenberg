from math import sqrt
from operator import add, sub, mul, div

class Color(object):

    @staticmethod
    def diff(color1, color2):
        diff_vector = map(sub, color1, color2)
        diff_scalar = sqrt(sum(map(mul, diff_vector, diff_vector)))
        return diff_scalar/sqrt(255**2 * 3)

    @staticmethod
    def diff_perceptive(color1, color2):
        diff_vector = map(sub, Color.to_Lab(color1), Color.to_Lab(color2))
        diff_scalar = sqrt(sum(map(mul, diff_vector, diff_vector)))
        return diff_scalar/100

    @staticmethod
    def avg(colors):
        total = (0.0, 0.0, 0.0)
        for color in colors:
            total = map(add, total, color)
        average = map(div, total, (color_count,)*3)
        return tuple(map(lambda x: int(round(x)), average))

    @staticmethod
    def avg_weighted(colors):
        total = (0.0, 0.0, 0.0)
        color_count = 0
        for (weight, color) in colors:
            color_count += weight
            weighted = map(mul, (weight,)*3, color)
            total = map(add, total, weighted)
        average = map(div, total, (color_count,)*3)
        return tuple(map(lambda x: int(round(x)), average))

    @staticmethod
    def to_Lab(color):
        from colormath.color_objects import LabColor, sRGBColor
        from colormath.color_conversions import convert_color
        return convert_color(
            sRGBColor(*color, is_upscaled=True),
            LabColor
        ).get_value_tuple()
