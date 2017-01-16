from .color_histogram import ColorHistogram

class Histogram(ColorHistogram):

    def get(self, resolution):
        self.image = self.image.convert('L')
        return super(Histogram, self).get(resolution)
