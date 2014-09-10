import unittest
from image_fingerprint import ImageFingerprint
import os

class ImageFingerprintTest(unittest.TestCase):

    def setUp(self):
        self.subject = ImageFingerprint()

    def test_generate(self):
        subject = ImageFingerprint(60, 30)
        self.assertEqual(subject.generate(os.path.join("test_images", "occult_small.jpg")),
                        {'total': (41, 41, 41), 'blocks': [[(33, 33, 33), (59, 59, 59)],
                                                           [(23, 23, 23), (49, 49, 49)]]}
                        )

if __name__ == "__main__":
    unittest.main()
