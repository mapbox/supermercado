import super_utils as sutils
import numpy as np
import mercantile
from affine import Affine

from rasterio import features

def project_geom(geom):
    return {
        'type': geom['type'],
        'coordinates': [
            [mercantile.xy(*coords) for coords in part]
            for part in geom['coordinates']
        ]
    }


def find_extrema(features):
    epsilon = 1.0e-10

    totalArr = np.array([c for f in features for poly in f['geometry']['coordinates'] for c in poly for poly in f])

    xMax = totalArr[:, 0].max() - epsilon
    xMin = totalArr[:, 0].min() + epsilon
    yMax = totalArr[:, 1].max() - epsilon
    yMin = totalArr[:, 1].min() + epsilon

    return [xMin, yMin, xMax, yMax]

def tile_extrema(bounds, zoom):
    minimumTile = mercantile.tile(bounds[0], bounds[3], zoom)
    maximumTile = mercantile.tile(bounds[2], bounds[1], zoom)

    return {
        'x': {
            'min': minimumTile.x,
            'max': maximumTile.x + 1
            },
        'y': {
            'min': minimumTile.y,
            'max': maximumTile.y + 1
            }
        }

def make_transform(tilerange, zoom):
    ulx, uly = mercantile.xy(*mercantile.ul(tilerange['x']['min'], tilerange['y']['min'], zoom))
    lrx, lry = mercantile.xy(*mercantile.ul(tilerange['x']['max'], tilerange['y']['max'], zoom))
    xcell = (lrx - ulx) / float(tilerange['x']['max'] - tilerange['x']['min'])
    ycell = (uly - lry) / float(tilerange['y']['max'] - tilerange['y']['min'])
    return Affine(xcell, 0, ulx,
        0, -ycell, uly)


def burn(polys, zoom):
    bounds = find_extrema(polys)
    tilerange = tile_extrema(bounds, zoom)
    afftrans = make_transform(tilerange, zoom)

    burn = features.rasterize(
            ((project_geom(geom['geometry']), 255) for geom in polys),
            out_shape=((tilerange['y']['max'] - tilerange['y']['min'], tilerange['x']['max'] - tilerange['x']['min'])),
            transform=afftrans,
            all_touched=True)

    xys = np.fliplr(np.dstack(np.where(burn))[0])

    xys[:, 0] += tilerange['x']['min']
    xys[:, 1] += tilerange['y']['min']

    return np.append(xys, np.zeros((xys.shape[0], 1), dtype=np.uint8) + zoom, axis=1)

