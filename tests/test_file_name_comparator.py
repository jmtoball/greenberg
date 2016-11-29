import unittest
from greenberg.comparators import FileNameComparator
from .util import img_path

class FileNameComparatorTest(unittest.TestCase):

    def setUp(self):
        self.subject = FileNameComparator
        print self.subject

    def test_identical(self):
        result = self.subject('/tmp/foo.jpg', '/tmp/foo.jpg').compare()
        self.assertEqual(result, 1.0)

    def test_different(self):
        result = self.subject('/tmp/bar.bmp', '/tmp/foo.jpg').compare()
        self.assertLess(result, 0.5)

    def test_similar(self):
        result = self.subject('/tmp/foo.png', '/tmp/foo.jpg').compare()
        self.assertGreater(result, 0.5)
