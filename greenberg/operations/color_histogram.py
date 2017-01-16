from greenberg.operations import ImageOperation, BoxedOperation, ColorCountList
from greenberg.util import chunks, normalize


class ColorHistogram(ImageOperation, BoxedOperation):

    def buckets(self, colors, buckets):
        return normalize(map(sum, chunks(colors, buckets)), self.area())

    def get(self, resolution=5):
        colors = self.image.histogram()
        band_count = len(self.image.getbands())

        return map(
            lambda colors: self.buckets(colors, resolution),
            chunks(colors, band_count)
        )
