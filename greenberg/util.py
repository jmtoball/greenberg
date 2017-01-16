from math import ceil

def chunk(items, chunk_size, idx):
    start = idx*chunk_size
    end = (idx + 1) * chunk_size
    return items[idx * chunk_size:(idx + 1) * chunk_size]


def chunks(items, chunk_count):
    chunk_size = int(ceil(len(items)/float(chunk_count)))
    return [chunk(items, chunk_size, idx) for idx in range(chunk_count)]


def normalize(items, maximum):
    return [x / float(maximum) for x in items]
