import numpy as np
import pytest
from supermercado import super_utils as sutils
from supermercado.burntiles import find_extrema


def test_get_range():
    xyzs = np.zeros((10, 3), dtype=int)

    xMinR, xMaxR, yMinR, yMaxR = np.random.randint(0, 100, 4)

    xMaxR += xMinR
    yMaxR += yMinR

    xMaxIdx, yMaxIdx = np.random.randint(0, 9, 2)

    xyzs[:, 0] = xMinR
    xyzs[:, 1] = yMinR

    xyzs[xMaxIdx, 0] = xMaxR
    xyzs[yMaxIdx, 1] = yMaxR

    xmin, xmax, ymin, ymax = sutils.get_range(xyzs)

    assert xmin == xMinR
    assert xmax == xMaxR
    assert ymin == yMinR
    assert ymax == yMaxR


def test_get_zoom():
    xyzs = np.zeros((10, 3), dtype=int)

    zRand = np.random.randint(1, 100, 1)[0]
    xyzs[:, 2] = zRand

    assert sutils.get_zoom(xyzs) == zRand


def test_get_zoom_fails_multiple_zooms():
    xyzs = np.zeros((10, 3), dtype=int)

    zRand = np.random.randint(1, 100, 1)[0]
    xyzs[:, 2] = zRand

    xyzs[2, 2] = zRand + 1

    with pytest.raises(ValueError):
        sutils.get_zoom(xyzs)


def test_get_zoom_fails_bad_dims_small():
    xyzs = np.zeros((10, 2))

    with pytest.raises(ValueError):
        sutils.get_zoom(xyzs)


def test_get_zoom_fails_bad_dims_big():
    xyzs = np.zeros((10, 4))

    with pytest.raises(ValueError):
        sutils.get_zoom(xyzs)


def test_filter_features_polygon():
    """Polygon should go through unfiltered"""
    features = [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 1]]],
            },
        }
    ]

    assert list(sutils.filter_features(features)) == features


def test_filter_features_linestring():
    """LineString should go through unfiltered"""
    features = [
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [[0, 0], [1, 0], [1, 1], [0, 1], [0, 1]],
            },
        }
    ]

    assert list(sutils.filter_features(features)) == features


def test_filter_features_point():
    """Points should go through unfiltered"""
    features = [
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [[0, 0]]}}
    ]

    assert list(sutils.filter_features(features)) == features


def test_filter_features_multi_polygon():
    """MultiPolygons should be turned into multiple Polygons"""
    features = [
        {
            "type": "Feature",
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [
                    [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 1]]],
                    [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 1]]],
                ],
            },
        }
    ]
    expected = [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 1]]],
            },
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 1]]],
            },
        },
    ]
    assert list(sutils.filter_features(features)) == expected


def test_filter_features_multi_point():
    """MultiPoints should be turned into multiple Points"""
    features = [
        {
            "type": "Feature",
            "geometry": {"type": "MultiPoint", "coordinates": [[0, 0], [1, 0]]},
        }
    ]
    expected = [
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [0, 0]}},
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [1, 0]}},
    ]
    assert list(sutils.filter_features(features)) == expected


def test_filter_features_multi_linstrings():
    """MultiLineStrings should be turned into multiple LineStrings"""
    features = [
        {
            "type": "Feature",
            "geometry": {
                "type": "MultiLineString",
                "coordinates": [
                    [[0, 0], [1, 0], [1, 1], [0, 1], [0, 1]],
                    [[0, 0], [1, 0], [1, 1], [0, 1], [0, 1]],
                ],
            },
        }
    ]
    expected = [
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [[0, 0], [1, 0], [1, 1], [0, 1], [0, 1]],
            },
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [[0, 0], [1, 0], [1, 1], [0, 1], [0, 1]],
            },
        },
    ]
    assert list(sutils.filter_features(features)) == expected


def test_find_extrema():
    """Extrema should be calculated correctly"""
    features = [
        {
            "geometry": {
                "coordinates": [
                    [-127.97, 49.15],
                    [-101.95, -8.41],
                    [-43.24, -32.84],
                    [37.62, -25.17],
                    [71.72, -7.01],
                    [107.23, 48.69],
                ],
                "type": "LineString",
            },
            "properties": {},
            "type": "Feature",
        },
        {
            "geometry": {
                "coordinates": [[-98.09, 61.44], [-46.76, 61.1]],
                "type": "LineString",
            },
            "properties": {},
            "type": "Feature",
        },
        {
            "geometry": {
                "coordinates": [[-6.33, 59.89], [59.06, 59.89]],
                "type": "LineString",
            },
            "properties": {},
            "type": "Feature",
        },
    ]
    bounds = find_extrema(features)

    assert bounds == (
        -127.9699999999,
        -32.8399999999,
        107.2299999999,
        61.439999999899996,
    )


def test_find_extrema_cross_antimeridian():
    """Extrema should be calculated correctly"""
    features = [
        {
            "geometry": {
                "coordinates": [
                    [-190.01, 49.15],
                    [-101.95, -8.41],
                    [-43.24, -32.84],
                    [37.62, -25.17],
                    [71.72, -7.01],
                    [190.01, 48.69],
                ],
                "type": "LineString",
            },
            "properties": {},
            "type": "Feature",
        },
        {
            "geometry": {
                "coordinates": [[-98.09, 61.44], [-46.76, 61.1]],
                "type": "LineString",
            },
            "properties": {},
            "type": "Feature",
        },
        {
            "geometry": {
                "coordinates": [[-6.33, 59.89], [59.06, 59.89]],
                "type": "LineString",
            },
            "properties": {},
            "type": "Feature",
        },
    ]
    bounds = find_extrema(features)

    assert bounds == (
        -190.0099999999,
        -32.8399999999,
        190.0099999999,
        61.439999999899996,
    )


def test_find_extrema_clipped_northsouth():
    """Extrema should be calculated correctly"""
    features = [
        {
            "geometry": {
                "coordinates": [
                    [-190.01, 90],
                    [-101.95, -8.41],
                    [-43.24, -32.84],
                    [37.62, -25.17],
                    [71.72, -7.01],
                    [190.01, -90],
                ],
                "type": "LineString",
            },
            "properties": {},
            "type": "Feature",
        },
        {
            "geometry": {
                "coordinates": [[-98.09, 61.44], [-46.76, 61.1]],
                "type": "LineString",
            },
            "properties": {},
            "type": "Feature",
        },
        {
            "geometry": {
                "coordinates": [[-6.33, 59.89], [59.06, 59.89]],
                "type": "LineString",
            },
            "properties": {},
            "type": "Feature",
        },
    ]
    bounds = find_extrema(features)

    assert bounds == (
        -190.0099999999,
        -85.0511287798066,
        190.0099999999,
        85.0511287798066,
    )
