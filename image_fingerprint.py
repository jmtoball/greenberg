from PIL import Image
from itertools import product

class ImageFingerprint(object):

    def __init__(self, image_size=300, block_size=30):
        self.IMAGE_SIZE = image_size
        self.BLOCK_SIZE = block_size

    def _prepare_image(self, path):
        img = Image.open(path)
        img = img.convert('RGB')
        shortest_side = min(img.size)
        cropped = img.crop((0, 0, shortest_side, shortest_side))
        resized = cropped.resize((self.IMAGE_SIZE, self.IMAGE_SIZE), Image.ANTIALIAS)
        return resized

    def _get_average_color(self, img, block_x, block_y):
        offset_y = block_y*self.BLOCK_SIZE
        offset_x = block_x*self.BLOCK_SIZE
        block = img.crop((offset_x, offset_y, offset_x+self.BLOCK_SIZE, offset_y+self.BLOCK_SIZE))
        block_pixels = self.BLOCK_SIZE**2
        colors = block.getcolors(block_pixels)
        block_agg = (0,0,0)
        for color in colors:
            quantified = tuple(map(lambda c: color[0]*c, color[1]))
            block_agg = map(sum, zip(block_agg, quantified))
        return tuple(map(lambda v: v/block_pixels, block_agg))

    def generate(self, path):
        img = self._prepare_image(path)
        blocks = self.IMAGE_SIZE/self.BLOCK_SIZE
        footprint = []
        total_agg = (0,0,0)
        for block_y in range(blocks):
            footprint.append([])
            for block_x in range(blocks):
                block_avg = self._get_average_color(img, block_x, block_y)
                footprint[block_y].append(block_avg)
                total_agg = map(sum, zip(total_agg, block_avg))
        total_avg = tuple(map(lambda v: v/(blocks**2), total_agg))
        return {"total": total_avg, "blocks": footprint}

    def compare(self, footprint_a, footprint_b):
        footprint_a = footprint_a['blocks']
        footprint_b = footprint_b['blocks']
        blocks_y = len(footprint_a)
        blocks_x = len(footprint_a[0])
        matches = 0
        for block_y, block_x in product(range(blocks_y), range(blocks_x)):
            if footprint_a[block_y][block_x] == footprint_b[block_y][block_x]:
                matches += 1
        total_blocks = blocks_x*blocks_y
        return (matches, total_blocks, matches/float(total_blocks))

    def similarity(self, footprint_a, footprint_b):
        return self.compare(footprint_a, footprint_b)[2]

    def output(self, footprint, path):
        from PIL import ImageDraw
        footprint = footprint['blocks']
        blocks_y = len(footprint)
        blocks_x = len(footprint[0])
        out = Image.new('RGB', (self.IMAGE_SIZE, self.IMAGE_SIZE))
        drawer = ImageDraw.Draw(out)
        for block_y, block_x in product(range(blocks_y), range(blocks_x)):
            offset_x = block_x * self.BLOCK_SIZE
            offset_y = block_y * self.BLOCK_SIZE
            drawer.rectangle((offset_x, offset_y, offset_x+self.BLOCK_SIZE, offset_y+self.BLOCK_SIZE), footprint[block_y][block_x])
        out.save(path)
