import numpy as np

import json, re

def parseString(tilestring, matcher):
    tile = [int(r) for r in matcher.match(tilestring).group().split('-')]
    tile.append(tile.pop(0))
    return tile

def getRange(xyz):
    return xyz[:, 0].min(), xyz[:, 0].max(), xyz[:, 1].min(), xyz[:, 1].max()

def burnXYZs(tiles, xmin, xmax, ymin, ymax, pad=1):
    # make an array of shape (xrange + 3, yrange + 3)
    burn = np.zeros((xmax - xmin + (pad * 2 + 1), ymax - ymin + (pad * 2 + 1)), dtype=bool)

    # using the tile xys as indicides, burn in True where a tile exists
    burn[(tiles[:,0] - xmin + pad, tiles[:, 1] - ymin + pad)] = True

    return burn


def tileParser(tiles, parsenames=False):
    if parsenames:
        tMatch = re.compile(r"[\d]+-[\d]+-[\d]+")
        tiles = np.array([parseString(t, tMatch) for t in tiles])
    else:
        tiles = np.array([json.loads(t) for t in tiles])

    return tiles

def getZoom(tiles):
    t, d = tiles.shape
    if t < 1 or d != 3:
        raise ValueError("Tiles must be of shape n, 3")

    if tiles[:, 2].min() != tiles[:, 2].max():
        raise ValueError("All tile zooms must be the same")

    return tiles[0, 2]
