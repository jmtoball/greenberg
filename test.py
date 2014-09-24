import unittest
from image_fingerprint import ImageFingerprint
import os

class ImageFingerprintTest(unittest.TestCase):

    def setUp(self):
        self.subject = ImageFingerprint()

    def test_generate(self):
        subject = ImageFingerprint(60, 30)
        self.assertEqual(subject.generate(os.path.join("test_images", "occult_small.jpg")),
                        {'total': (42, 42, 42), 'blocks': [[(35, 35, 35), (50, 50, 50)]]}
                        )

    def test_compare_scaled(self):
        a = self.subject.generate(os.path.join("test_images", "occult_grey.jpg"))
        b = self.subject.generate(os.path.join("test_images", "occult_small.jpg"))
        atob = self.subject.compare(a, b)
        btoa = self.subject.compare(b, a)
        self.assertLess(atob.similarity, 1)
        self.assertGreater(atob.similarity, 0.95)
        self.assertEqual(atob.similarity, btoa.similarity)

    def test_compare_different(self):
        a = self.subject.generate(os.path.join("test_images", "occult_small.jpg"))
        b = self.subject.generate(os.path.join("test_images", "occult_small_changed.jpg"))
        atob = self.subject.compare(a, b)
        btoa = self.subject.compare(b, a)
        self.assertLess(atob.similarity, 1)
        self.assertGreater(atob.similarity, 0.925)
        self.assertEqual(atob.similarity, btoa.similarity)

    def test_compare_horizontal_crop(self):
        a = self.subject.generate(os.path.join("test_images", "occult_small.jpg"))
        b = self.subject.generate(os.path.join("test_images", "occult_small_cropped.jpg"))
        atob = self.subject.compare(a, b)
        btoa = self.subject.compare(b, a)
        self.assertGreater(atob.similarity, 0.05)
        self.assertEqual(atob.similarity, btoa.similarity)

    def test_compare_vertical_crop(self):
        a = self.subject.generate(os.path.join("test_images", "occult_small.jpg"))
        b = self.subject.generate(os.path.join("test_images", "occult_small_cropped_2.jpg"))
        atob = self.subject.compare(a, b)
        btoa = self.subject.compare(b, a)
        self.assertLess(atob.similarity, 1)
        self.assertGreater(atob.similarity, 0.006)
        self.assertEqual(atob.similarity, btoa.similarity)

    @unittest.skip("Enter img_dir to run this test")
    def test_benchmark(self):
        import os
        from os import path
        fp = ImageFingerprint()
        img_dir = "Enter path!"
        files = []

        for file_name in os.listdir(img_dir):
            if path.isfile(path.join(img_dir, file_name)):
                files.append(file_name)

        footprints = {}
        for file_name in files:
            footprints[file_name] = fp.generate(path.join(img_dir, file_name))

        for a in footprints.keys():
            fp.output(footprints[a], ("/tmp/" + a).replace(".jpg", ".png").replace(".gif", ".png"))
            for b in footprints.keys():
                comp = fp.compare(footprints[a],footprints[b])
                if comp.similarity > 0.7 and a != b:
                    print a, b, comp.__dict__
                    print "!"*25


if __name__ == "__main__":
    unittest.main()
