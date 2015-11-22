import click, json, re

import numpy as np

import super_utils as sutils

def getRange(xyz):
    return xyz[:, 0].min(), xyz[:, 0].max(), xyz[:, 1].min(), xyz[:, 1].max()

def getIdx():
    tt = np.zeros((3, 3), dtype=bool)
    tt[1, 1] = True

    return np.dstack(np.where(tt != True))[0] - 1

def parseString(tilestring, matcher):
    tile = [int(r) for r in matcher.match(tilestring).group().split('-')]
    tile.append(tile.pop(0))
    return tile

def findedges(inputtiles, parsenames):


    tiles = sutils.tileParser(inputtiles, parsenames)

    xmin, xmax, ymin, ymax = getRange(tiles)

    zoom = sutils.getZoom(tiles)
    # zoom = inputtiles[0, -1]

    # make an array of shape (xrange + 3, yrange + 3)
    burn = sutils.burnXYZs(tiles, xmin, xmax, ymin, ymax)

    # Create the indixes for rolling
    idxs = getIdx()

    # Using the indices to roll + stack the array, find the minimum along the rolled / stacked axis
    xys_edge = (np.min(np.dstack((
        np.roll(np.roll(burn, i[0], 0), i[1], 1) for i in idxs
        )), axis=2) - burn)

    # Set missed non-tiles to False
    xys_edge[burn == False] = False

    # Recreate the tile xyzs, and add the min vals
    xys_edge = np.dstack(np.where(xys_edge))
    xys_edge[0, :, 0] += xmin - 1
    xys_edge[0, :, 1] += ymin - 1

    # Echo out the results
    return xys_edge[0], zoom



# if __name__ == '__main__':
#     findedges(["[0, 0, 1]","[0, 1, 1]","[1, 0, 1]","[1, 1, 1]"], False)