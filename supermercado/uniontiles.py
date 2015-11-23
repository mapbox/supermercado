import json, click

import super_utils as sutils
from rasterio import features, Affine
import mercantile

import numpy as np


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

def union(inputtiles, parsenames):

    tiles = sutils.tileParser(inputtiles, parsenames)

    xmin, xmax, ymin, ymax = sutils.getRange(tiles)

    zoom = sutils.getZoom(tiles)

    # make an array of shape (xrange + 3, yrange + 3)
    burn = sutils.burnXYZs(tiles, xmin, xmax, ymin, ymax, 0)

    nw = mercantile.xy(*mercantile.ul(xmin, ymin, zoom))

    se = mercantile.xy(*mercantile.ul(xmax + 1, ymax + 1, zoom))

    aff = Affine(((se[0] - nw[0]) / float(xmax - xmin + 1)), 0.0, nw[0],
        0.0, -((nw[1] - se[1]) / float(ymax - ymin + 1)), nw[1])

    unprojecter = Unprojecter()

    unionedTiles = [{'geometry': unprojecter.unproject(feature)} for feature, shapes in features.shapes(np.asarray(np.flipud(np.rot90(burn)).astype(np.uint8), order='C'), transform=aff) if shapes == 1]

    return unionedTiles


if __name__ == '__main__':
    union()

