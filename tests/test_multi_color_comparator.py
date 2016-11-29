import unittest
from greenberg.comparators import MultiColorComparator
from greenberg.operations import ProminentColors
from .util import img_path

class MultiColorComparatorTest(object):

    subject = MultiColorComparator

    def test_identical(self):
        result = self.subject(
            img_path(self.file_prefix + '.png'),
            img_path(self.file_prefix + '_identical.png'),
            self.operation
        ).compare()
        self.assertGreater(result, 0.95)

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

class DominantColorComparatorTest(unittest.TestCase, MultiColorComparatorTest):
    file_prefix = 'prominent_colors'
    operation = ProminentColors
