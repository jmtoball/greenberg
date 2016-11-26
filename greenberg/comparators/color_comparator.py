from math import sqrt
from operator import sub, mul

class ColorComparator(object):

    def color_diff(self, color1, color2):
        diff_vector = map(sub, color1, color2)
        diff_scalar = sqrt(sum(map(mul, diff_vector, diff_vector)))
        return diff_scalar/sqrt(255**2 * 3)
