import super_utils as sutils
import numpy as np
import mercantile
from affine import Affine

from rasterio import features

def find_extrema(features):
    epsilon = 1.0e-10
    # epsilon = 0
    totalArr = np.array([c for f in features for poly in f['geometry']['coordinates'] for c in poly for poly in f])
    xMax = totalArr[:, 0].max() + epsilon
    xMin = totalArr[:, 0].min() - epsilon
    yMax = totalArr[:, 1].max() + epsilon
    yMin = totalArr[:, 1].min() - epsilon
    return [xMin, yMin, xMax, yMax]

def tile_extrema(bounds, zoom):
    minimumTile = mercantile.tile(bounds[0], bounds[3], zoom)
    maximumTile = mercantile.tile(bounds[2], bounds[1], zoom)
    return {
        'x': {
            'min': minimumTile.x,
            'max': maximumTile.x
            },
        'y': {
            'min': minimumTile.y,
            'max': maximumTile.y
            }
        }

def make_transform(tilerange, zoom):
    ul = mercantile.ul(tilerange['x']['min'], tilerange['y']['min'], zoom)
    lr = mercantile.ul(tilerange['x']['max'], tilerange['y']['max'], zoom)
    xcell = (lr.lng - ul.lng) / float(tilerange['x']['max'] - tilerange['x']['min'])
    ycell = (ul.lat - lr.lat) / float(tilerange['y']['max'] - tilerange['y']['min'])
    return Affine(xcell, 0, ul.lng,
        0, -ycell, ul.lat)


def burn(polys, zoom):
    bounds = find_extrema(polys)
    tilerange = tile_extrema(bounds, zoom)
    afftrans = make_transform(tilerange, zoom)

    burn = features.rasterize(
            ((geom['geometry'], 255) for geom in polys),
            out_shape=((tilerange['y']['max'] - tilerange['y']['min'] + 1, tilerange['x']['max'] - tilerange['x']['min'] + 1)),
            transform=afftrans,
            all_touched=True)

    xys = np.fliplr(np.dstack(np.where(burn))[0])

    xys[:, 0] += tilerange['x']['min']
    xys[:, 1] += tilerange['y']['min']

    return xys

