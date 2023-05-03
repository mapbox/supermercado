import numpy as np

from supermercado import super_utils as sutils
from rasterio import features, Affine
import mercantile


def create_density(tiles, xmin, xmax, ymin, ymax, pad=1):
    """Given an ndarray or tiles and range,
    create a density raster of tile frequency
    """
    burn = np.zeros(
        (xmax - xmin + (pad * 2 + 1), ymax - ymin + (pad * 2 + 1)), dtype=np.uint32
    )

    tiles, counts = np.unique(tiles, return_counts=True, axis=0)

    burn[(tiles[:, 0] - xmin + pad, tiles[:, 1] - ymin + pad)] = counts

    return burn


def heatmap(inputtiles, parsenames):
    """Creates a vector "heatmap" of tile densities

    Parameters
    ----------
    inputtiles: sequence of [x, y, z] or strings
        tiles to create a density heatmap from
    parsenames: boolean
        parse tile names from strings

    Returns
    -------
    density_features: generator
        sequence of features
    """
    tiles = sutils.tile_parser(inputtiles, parsenames)

    xmin, xmax, ymin, ymax = sutils.get_range(tiles)

    zoom = sutils.get_zoom(tiles)

    # make an array of shape (xrange + 3, yrange + 3)
    burn = sutils.burnXYZs(tiles, xmin, xmax, ymin, ymax, 0)

    nw = mercantile.xy(*mercantile.ul(xmin, ymin, zoom))

    se = mercantile.xy(*mercantile.ul(xmax + 1, ymax + 1, zoom))

    aff = Affine(
        ((se[0] - nw[0]) / float(xmax - xmin + 1)),
        0.0,
        nw[0],
        0.0,
        -((nw[1] - se[1]) / float(ymax - ymin + 1)),
        nw[1],
    )

    unprojecter = sutils.Unprojecter()

    density = create_density(tiles, xmin, xmax, ymin, ymax)

    density = np.asarray(np.flipud(np.rot90(density)).astype(np.uint8), order="C")

    density_features = (
        {
            "geometry": unprojecter.unproject(feature),
            "properties": {"n": count},
            "type": "Feature",
        }
        for feature, count in features.shapes(
            density,
            mask=density > 0,
            transform=aff,
        )
    )

    return density_features
