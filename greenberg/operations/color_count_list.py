from greenberg.operations import ImageOperation, BoxedOperation

class ColorCountList(ImageOperation, BoxedOperation):

    def get(self):
        return self.image.crop(self.box()).getcolors(self.area())
