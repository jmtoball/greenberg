import unittest
from greenberg.comparators import ColorComparator
from greenberg.operations import DominantColor, AverageColor
from .util import img_path

class ColorComparatorTest(object):

    subject = ColorComparator

    def test_identical(self):
        result = self.subject(
            img_path(self.file_prefix + '.png'),
            img_path(self.file_prefix + '_identical.png'),
            self.operation
        ).compare()
        self.assertEqual(result, 1.0)

    def test_different(self):
        result = self.subject(
            img_path(self.file_prefix + '.png'),
            img_path(self.file_prefix + '_different.png'),
            self.operation
        ).compare()
        self.assertLess(result, 0.5)

    def test_similar(self):
        result = self.subject(
            img_path(self.file_prefix + '.png'),
            img_path(self.file_prefix + '_similar.png'),
            self.operation
        ).compare()
        self.assertGreater(result, 0.5)

class DominantColorComparatorTest(unittest.TestCase, ColorComparatorTest):
    file_prefix = 'dominant_color'
    operation = DominantColor

class AverageColorComparatorTest(unittest.TestCase, ColorComparatorTest):
    file_prefix = 'average_color'
    operation = AverageColor
