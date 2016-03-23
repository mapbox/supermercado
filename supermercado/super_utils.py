import numpy as np

import json, re, mercantile

def parseString(tilestring, matcher):
    tile = [int(r) for r in matcher.match(tilestring).group().split('-')]
    tile.append(tile.pop(0))
    return tile

def get_range(xyz):
    return xyz[:, 0].min(), xyz[:, 0].max(), xyz[:, 1].min(), xyz[:, 1].max()

def burnXYZs(tiles, xmin, xmax, ymin, ymax, pad=1):
    # make an array of shape (xrange + 3, yrange + 3)
    burn = np.zeros((xmax - xmin + (pad * 2 + 1), ymax - ymin + (pad * 2 + 1)), dtype=bool)

    # using the tile xys as indicides, burn in True where a tile exists
    burn[(tiles[:,0] - xmin + pad, tiles[:, 1] - ymin + pad)] = True

    return burn


def tile_parser(tiles, parsenames=False):
    if parsenames:
        tMatch = re.compile(r"[\d]+-[\d]+-[\d]+")
        tiles = np.array([parseString(t, tMatch) for t in tiles])
    else:
        tiles = np.array([json.loads(t) for t in tiles])

    return tiles

def get_idx():
    tt = np.zeros((3, 3), dtype=bool)
    tt[1, 1] = True

    return np.dstack(np.where(tt != True))[0] - 1

def get_zoom(tiles):
    t, d = tiles.shape
    if t < 1 or d != 3:
        raise ValueError("Tiles must be of shape n, 3")

    if tiles[:, 2].min() != tiles[:, 2].max():
        raise ValueError("All tile zooms must be the same")

    return tiles[0, 2]

def filter_polygons(features):
    for f in features:
        if 'geometry' in f and 'type' in f['geometry']:
            if f['geometry']['type'] == 'Polygon':
                yield f
            elif f['geometry']['type'] == 'MultiPolygon':
                for part in f['geometry']['coordinates']:
                    yield {
                        'geometry': {
                            'type': 'Polygon',
                            'coordinates': part
                        }
                    }

class Unprojecter:
    def __init__(self):
        self.R2D = 180 / np.pi
        self.A = 6378137.0

    def xy_to_lng_lat(self, coordinates):
        for c in coordinates:
            tc = np.array(c)
            yield np.dstack([
                tc[:, 0] * self.R2D / self.A,
                ((np.pi * 0.5) - 2.0 * np.arctan(np.exp(-tc[:, 1] / self.A))) * self.R2D
                ])[0].tolist()

    def unproject(self, feature):
        feature['coordinates'] = [f for f in self.xy_to_lng_lat(feature['coordinates'])]
        return feature
