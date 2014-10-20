import unittest
from image_fingerprint import ImageFingerprint, ImageHistogram
import os
from os import path

class ImageComparatorTest(unittest.TestCase):

    def compare(self, a, b, min_diff, max_diff):
        a = self.subject.generate(os.path.join("test_images", a))
        b = self.subject.generate(os.path.join("test_images", b))
        atob = self.subject.compare(a, b)
        btoa = self.subject.compare(b, a)
        self.assertLess(atob.similarity, max_diff)
        self.assertGreater(atob.similarity, min_diff)
        self.assertEqual(atob.similarity, btoa.similarity)

class ImageFingerprintTest(ImageComparatorTest):

    def setUp(self):
        self.subject = ImageFingerprint()

    def test_generate(self):
        subject = ImageFingerprint(60, 30)
        self.assertEqual(subject.generate(os.path.join("test_images", "occult_small.jpg")),
                        {'total': (42, 42, 42), 'blocks': [[(35, 35, 35), (50, 50, 50)]]}
                        )

    def test_compare_scaled(self):
        self.compare("occult_grey.jpg", "occult_small.jpg", 0.95, 1)

    def test_compare_different(self):
        self.compare("occult_small.jpg", "occult_small_changed.jpg", 0.925, 1)

    def test_compare_horizontal_crop(self):
        self.compare("occult_small.jpg", "occult_small_cropped.jpg", 0.05, 1)

    def test_compare_vertical_crop(self):
        self.compare("occult_small.jpg", "occult_small_cropped_2.jpg", 0.006, 1)

    @unittest.skip("tooo fucking long")
    def test_benchmark(self):
        img_dir = '/home/max/Pictures/Sammlung/Obskur'
        files = []

        for file_name in os.listdir(img_dir):
            if path.isfile(path.join(img_dir, file_name)):
                files.append(file_name)

        footprints = {}
        for file_name in files:
            footprints[file_name] = self.subject.generate(path.join(img_dir, file_name))

        for a in footprints.keys():
            self.subject.output(footprints[a], ("/tmp/" + a).replace(".jpg", ".png").replace(".gif", ".png"))
            for b in footprints.keys():
                comp = self.subjectfp.compare(footprints[a],footprints[b])
                if comp.similarity > 0.7 and a != b:
                    print a, b, comp.__dict__
                    print "!"*25


class ImageHistogramTest(ImageComparatorTest):

    def setUp(self):
        self.subject = ImageHistogram()

    def test_compare_recolored(self):
        self.compare("occult_grey.jpg", "occult.jpg", 0.9, 1)

    def test_compare_scaled(self):
        self.compare("occult_grey.jpg", "occult_small.jpg", 0.9, 1)

    def test_compare_small_differences(self):
        self.compare("occult_small.jpg", "occult_small_changed.jpg", 0.90, 0.95)

    def test_compare_mirrored(self):
        self.compare("occult_small.jpg", "occult_small_mirrored.jpg", 0.999, 1.01)

    def test_benchmark(self):
        img_dir = '/home/max/Pictures/Sammlung/Obskur'
        files = []

        for file_name in os.listdir(img_dir):
            if path.isfile(path.join(img_dir, file_name)):
                files.append(file_name)

        footprints = {}
        for file_name in files:
            footprints[file_name] = self.subject.generate(path.join(img_dir, file_name))

        for a in footprints.keys():
            for b in footprints.keys():
                comp = self.subject.compare(footprints[a],footprints[b], tolerance=0.005)
                if comp.similarity > 0.90 and a != b:
                    print a, b, comp.__dict__
                    print "!"*25

if __name__ == "__main__":
    unittest.main()
