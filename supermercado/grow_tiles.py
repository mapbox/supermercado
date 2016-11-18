from supermercado import super_utils as sutils
import numpy as np


def itergrow(burn, distance=1):
    idxs = sutils.get_idx()

    for g in range(distance):
        burn = (np.max(np.dstack((
            np.roll(np.roll(burn, i[0], 0), i[1], 1) for i in idxs
            )), axis=2)) 

    return burn

def grow(inputtiles, parsenames, distance):
    tiles = sutils.tile_parser(inputtiles, parsenames)

    xmin, xmax, ymin, ymax = sutils.get_range(tiles)

    zoom = sutils.get_zoom(tiles)

    burn = sutils.burnXYZs(tiles, xmin, xmax, ymin, ymax, pad=distance+1)

    xys_edge = itergrow(burn.copy(), distance) - burn

    xys_edge = np.dstack(np.where(xys_edge))[0]
    xys_edge[:, 0] += xmin - 1 - distance
    xys_edge[:, 1] += ymin - 1 - distance


    return np.append(xys_edge, np.zeros((xys_edge.shape[0], 1), dtype=np.uint8) + zoom, axis=1)