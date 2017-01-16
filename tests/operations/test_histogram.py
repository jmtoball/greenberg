import unittest
from greenberg.operations import ColorHistogram
from greenberg import Loader
from ..util import img_path


class ImageOperationTest(unittest.TestCase):

    def setUp(self):
        img = Loader.load(img_path(self.test_image))
        self.subject = self.tested_class(img)


class ColorHistogramOperationTest(ImageOperationTest):

    tested_class = ColorHistogram
    test_image = 'histogram.png'

    def test_band_count(self):
        band_count = len(self.subject.get(5))
        self.assertEqual(band_count, 3)

    def test_contents(self):
        res = self.subject.get(3)
        r = [0.75, 0.0, 0.25]
        self.assertListEqual(res[0], r)
        g = [0.75, 0.0, 0.25]
        self.assertListEqual(res[1], g)
        b = [0.75, 0.0, 0.25]
        self.assertListEqual(res[2], b)
