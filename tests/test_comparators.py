import unittest
from comparator import FileNameComparator, DominantColorComparator, AverageColorComparator
import os
from os import path

def img_path(name):
    return path.join('test_images', name)

class FileNameComparatorTest(unittest.TestCase):

    def setUp(self):
        self.subject = FileNameComparator()

    def test_identical(self):
        result = self.subject.compare('/tmp/foo.jpg', '/tmp/foo.jpg')
        self.assertEqual(result, 1.0)

    def test_different(self):
        result = self.subject.compare('/tmp/bar.bmp', '/tmp/foo.jpg')
        self.assertLess(result, 0.5)

    def test_similar(self):
        result = self.subject.compare('/tmp/foo.png', '/tmp/foo.jpg')
        self.assertGreater(result, 0.5)

class DominantColorComparatorTest(unittest.TestCase):

    def setUp(self):
        self.subject = DominantColorComparator()

    def test_identical(self):
        result = self.subject.compare(
            img_path('dominant_color.png'),
            img_path('dominant_color_identical.png')
        )
        self.assertEqual(result, 1.0)

    def test_different(self):
        result = self.subject.compare(
            img_path('dominant_color.png'),
            img_path('dominant_color_different.png')
        )
        self.assertLess(result, 0.25)

    def test_similar(self):
        result = self.subject.compare(
            img_path('dominant_color.png'),
            img_path('dominant_color_similar.png')
        )
        self.assertGreater(result, 0.75)

class AverageColorComparatorTest(unittest.TestCase):

    def setUp(self):
        self.subject = AverageColorComparator()

    def test_identical(self):
        result = self.subject.compare(
            img_path('average_color.png'),
            img_path('average_color_identical.png')
        )
        self.assertEqual(result, 1.0)

    def test_different(self):
        result = self.subject.compare(
            img_path('average_color.png'),
            img_path('average_color_different.png')
        )
        self.assertLess(result, 0.5)

    def test_similar(self):
        result = self.subject.compare(
            img_path('average_color.png'),
            img_path('average_color_similar.png')
        )
        self.assertGreater(result, 0.75)
