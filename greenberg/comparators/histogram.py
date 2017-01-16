from greenberg.comparators import ImageComparator
from operator import sub, mul
from itertools import chain


class HistogramComparator(ImageComparator):

    def __init__(self, path_one, path_two, histogram_operation, resolution=3):
        super(HistogramComparator, self).__init__(path_one, path_two)
        self.histogram_operation = histogram_operation
        self.resolution = resolution

    def compare(self):
        histograms = []
        for image in [self.image_one, self.image_two]:
            image_size = mul(*image.size)
            histograms.append(
                self.histogram_operation(image).get(self.resolution)
            )
        diff_vectors = map(sub, *map(chain.from_iterable, histograms))
        diff_scalars = map(abs, diff_vectors)
        return 1 - sum(diff_scalars)
