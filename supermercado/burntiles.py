"""Burntile."""

import mercantile
import numpy as np
from affine import Affine
from rasterio import features


def project_geom(geom):
    """Project geometry.

    Parameters
    ------------
    geom: geojson

    Returns
    ---------
    json
    """
    if geom["type"] == "Polygon":
        return {
            "type": geom["type"],
            "coordinates": [
                [mercantile.xy(*coords) for coords in part]
                for part in geom["coordinates"]
            ],
        }
    elif geom["type"] == "LineString":
        return {
            "type": geom["type"],
            "coordinates": [mercantile.xy(*coords) for coords in geom["coordinates"]],
        }
    elif geom["type"] == "Point":
        return {
            "type": geom["type"],
            "coordinates": mercantile.xy(*geom["coordinates"]),
        }


def _feature_extrema(geometry):
    """For each feature in geometry, return extrema."""
    if geometry["type"] == "Polygon":
        x, y = zip(*[c for part in geometry["coordinates"] for c in part])
    elif geometry["type"] == "LineString":
        x, y = zip(*[c for c in geometry["coordinates"]])
    elif geometry["type"] == "Point":
        x, y = geometry["coordinates"]
        return x, y, x, y

    return min(x), min(y), max(x), max(y)


def find_extrema(features):
    """For a collection of features, return extrema.

    Parameters
    ------------
    features: geojson

    Returns
    ---------
    tuple
    """
    epsilon = 1.0e-10
    min_x, min_y, max_x, max_y = zip(
        *[_feature_extrema(f["geometry"]) for f in features]
    )

    return (
        min(min_x) + epsilon,
        max(min(min_y) + epsilon, -85.0511287798066),
        max(max_x) - epsilon,
        min(max(max_y) - epsilon, 85.0511287798066),
    )


def tile_extrema(bounds, zoom):
    """For given bounds and zoom, return extrema.

    Parameters
    ------------
    bounds: tuple
        min(x), min(y), max(x), max(y)
    zoom: int
        Zoom level to burn.

    Returns
    ---------
    json
    """
    minimumTile = mercantile.tile(bounds[0], bounds[3], zoom)
    maximumTile = mercantile.tile(bounds[2], bounds[1], zoom)

    return {
        "x": {"min": minimumTile.x, "max": maximumTile.x + 1},
        "y": {"min": minimumTile.y, "max": maximumTile.y + 1},
    }


def make_transform(tilerange, zoom):
    """For given tilerange and zoom, create affine transformation.

    Parameters
    ------------
    tilerange: json
    zoom: int
        Zoom level to burn.

    Returns
    ---------
    Affine transformation object
    """
    ulx, uly = mercantile.xy(
        *mercantile.ul(tilerange["x"]["min"], tilerange["y"]["min"], zoom)
    )
    lrx, lry = mercantile.xy(
        *mercantile.ul(tilerange["x"]["max"], tilerange["y"]["max"], zoom)
    )
    xcell = (lrx - ulx) / float(tilerange["x"]["max"] - tilerange["x"]["min"])
    ycell = (uly - lry) / float(tilerange["y"]["max"] - tilerange["y"]["min"])
    return Affine(xcell, 0, ulx, 0, -ycell, uly)


def burn(polys, zoom):
    """For a given geometry and zoom, return tiles.

    Parameters
    ------------
    polys: geojson
    zoom: int
        Zoom level to burn.

    Returns
    ---------
    numpy array
    """
    bounds = find_extrema(polys)

    tilerange = tile_extrema(bounds, zoom)
    afftrans = make_transform(tilerange, zoom)

    burn = features.rasterize(
        ((project_geom(geom["geometry"]), 255) for geom in polys),
        out_shape=(
            (
                tilerange["y"]["max"] - tilerange["y"]["min"],
                tilerange["x"]["max"] - tilerange["x"]["min"],
            )
        ),
        transform=afftrans,
        all_touched=True,
    )

    xys = np.fliplr(np.dstack(np.where(burn))[0])

    xys[:, 0] += tilerange["x"]["min"]
    xys[:, 1] += tilerange["y"]["min"]

    return np.append(xys, np.zeros((xys.shape[0], 1), dtype=np.uint8) + zoom, axis=1)
