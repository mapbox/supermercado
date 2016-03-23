import click, json, re

import numpy as np

import super_utils as sutils

def findedges(inputtiles, parsenames):


    tiles = sutils.tile_parser(inputtiles, parsenames)

    xmin, xmax, ymin, ymax = sutils.get_range(tiles)

    zoom = sutils.get_zoom(tiles)
    # zoom = inputtiles[0, -1]

    # make an array of shape (xrange + 3, yrange + 3)
    burn = sutils.burnXYZs(tiles, xmin, xmax, ymin, ymax)

    # Create the indixes for rolling
    idxs = sutils.get_idx()

    # Using the indices to roll + stack the array, find the minimum along the rolled / stacked axis
    xys_edge = (np.min(np.dstack((
        np.roll(np.roll(burn, i[0], 0), i[1], 1) for i in idxs
        )), axis=2) - burn)

    # Set missed non-tiles to False
    xys_edge[burn == False] = False

    # Recreate the tile xyzs, and add the min vals
    xys_edge = np.dstack(np.where(xys_edge))[0]
    xys_edge[:, 0] += xmin - 1
    xys_edge[:, 1] += ymin - 1

    # Return the edge array

    return np.append(xys_edge, np.zeros((xys_edge.shape[0], 1), dtype=np.uint8) + zoom, axis=1)


if __name__ == '__main__':
    findedges()