from PIL import Image
from itertools import product

class FingerprintComparison(object):

    def __init__(self, matches, missing, blocks):
        self.similarity = matches/float(blocks)
        self.matches = matches
        self.missing = missing
        self.blocks = blocks

class ImageFingerprint(object):

    def __init__(self, image_size=500, block_size=25, tolerance=0.15):
        self.IMAGE_SIZE = image_size
        self.BLOCK_SIZE = block_size
        self.TOLERANCE = tolerance

    def _prepare_image(self, path):
        img = Image.open(path)
        img = img.convert('RGB')
        width = img.size[0]
        height = img.size[1]
        aspect = width/float(height)
        if aspect >= 1:
            new_width = self.IMAGE_SIZE
            new_height = int(round(new_width/aspect))
        else:
            new_height = self.IMAGE_SIZE
            new_width = int(round(new_height*aspect))
        resized = img.resize((new_width, new_height), Image.BICUBIC)
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
        blocks_w = img.size[0]/self.BLOCK_SIZE
        blocks_h = img.size[1]/self.BLOCK_SIZE
        footprint = []
        total_agg = (0,0,0)
        for block_y in range(blocks_h):
            footprint.append([])
            for block_x in range(blocks_w):
                block_avg = self._get_average_color(img, block_x, block_y)
                footprint[block_y].append(block_avg)
                total_agg = map(sum, zip(total_agg, block_avg))
        total_avg = tuple(map(lambda v: v/(blocks_w*blocks_h), total_agg))
        return {"total": total_avg, "blocks": footprint}

    def compare(self, footprint_a, footprint_b):
        footprint_a = footprint_a['blocks']
        footprint_b = footprint_b['blocks']
        blocks_y = max(len(footprint_a), len(footprint_b))
        blocks_x = max(len(footprint_a[0]), len(footprint_b[0]))
        matches = 0
        missing = 0
        for block_y, block_x in product(range(blocks_y), range(blocks_x)):
            try:
                rgb_pairs = zip(footprint_a[block_y][block_x], footprint_b[block_y][block_x])
                rgb_diff = map(lambda p: abs(p[0]-p[1]), rgb_pairs)
                abs_error = sum(rgb_diff)
                rel_error = abs_error/255.0

                if rel_error < self.TOLERANCE:
                    matches += 1
            except IndexError:
                missing += 1
        total_blocks = blocks_x*blocks_y
        return FingerprintComparison(matches, missing, total_blocks)

    def output(self, footprint, path):
        from PIL import ImageDraw
        footprint = footprint['blocks']
        blocks_y = len(footprint)
        blocks_x = len(footprint[0])
        out = Image.new('RGB', (blocks_x*self.BLOCK_SIZE, blocks_y*self.BLOCK_SIZE))
        drawer = ImageDraw.Draw(out)
        for block_y, block_x in product(range(blocks_y), range(blocks_x)):
            offset_x = block_x * self.BLOCK_SIZE
            offset_y = block_y * self.BLOCK_SIZE
            drawer.rectangle((offset_x, offset_y, offset_x+self.BLOCK_SIZE, offset_y+self.BLOCK_SIZE), footprint[block_y][block_x])
        out.save(path)
