import rasterio as rio

import super_utils as sutils
from rasterio import rio
import mercantile

def union(inputtiles, parsenames):

    tiles = sutils.tileParser(inputtiles, parsenames)

    xmin, xmax, ymin, ymax = sutils.getRange(tiles)

    zoom = sutils.getZoom(tiles)

    # make an array of shape (xrange + 3, yrange + 3)
    burn = sutils.burnXYZs(tiles, xmin, xmax, ymin, ymax)

    nw = mercantile.ul(xmin, ymin, zoom)

    se = mercantile.ul(xmax + 1, ymax + 1, zoom)

