from PIL import Image
class Loader(object):

    @staticmethod
    def load(path):
        return Image.open(path)
