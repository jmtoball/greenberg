from operator import itemgetter
from random import sample
from greenberg.operations import ImageOperation, BoxedOperation, ColorCountList
from greenberg import Color

class ProminentColors(ImageOperation, BoxedOperation):

    def get(self, amount=3):
        colors = ColorCountList(self.image).get()
        # TODO: Optimize the initial set of centroids using k-means++ algorithm
        centroids = map(itemgetter(1), sample(colors, amount))
        max_distance = 0
        prev_max_distance = None

        while max_distance != prev_max_distance:
            clusters = [[] for i in range(amount)]
            prev_max_distance = max_distance
            for color in colors:
                distances = [Color.diff(color[1], centroid) for centroid in centroids]
                max_distance = max(max_distance, max(distances))
                nearest_centroid = distances.index(min(distances))
                clusters[nearest_centroid].append(color)

            centroids = [Color.avg_weighted(cluster) for cluster in clusters]
        return sorted(centroids, key=itemgetter(1))
