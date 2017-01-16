import unittest
from greenberg.comparators import HistogramComparator
from greenberg.operations import ColorHistogram, Histogram
from .util import img_path


class HistogramComparatorTest(object):

    subject = HistogramComparator

    def test_identical(self):
        result = self.subject(
            img_path(self.file_prefix + '.jpg'),
            img_path(self.file_prefix + '_identical.jpg'),
            self.histogram_operation
        ).compare()
        self.assertGreater(result, 0.95)

    def test_different(self):
        result = self.subject(
            img_path(self.file_prefix + '.jpg'),
            img_path(self.file_prefix + '_different.jpg'),
            self.histogram_operation
        ).compare()
        self.assertLess(result, 0.3)

    def test_similar(self):
        result = self.subject(
            img_path(self.file_prefix + '.jpg'),
            img_path(self.file_prefix + '_similar.jpg'),
            self.histogram_operation
        ).compare()
        self.assertGreater(result, 0.75)


class ColorHistogramComparatorTest(unittest.TestCase, HistogramComparatorTest):

    file_prefix = 'color_histogram'
    histogram_operation = ColorHistogram


class MonochromeHistogramComparatorTest(unittest.TestCase,
                                        HistogramComparatorTest):

    file_prefix = 'histogram'
    histogram_operation = Histogram
