import numpy as np
import pytest

from supermercado import super_utils as sutils


def test_get_range():
    """Test range."""
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
    """Test zoom."""
    xyzs = np.zeros((10, 3), dtype=int)

    zRand = np.random.randint(1, 100, 1)[0]
    xyzs[:, 2] = zRand

    assert sutils.get_zoom(xyzs) == zRand


def test_get_zoom_fails_multiple_zooms():
    """Multiple zoom should fail."""
    xyzs = np.zeros((10, 3), dtype=int)

    zRand = np.random.randint(1, 100, 1)[0]
    xyzs[:, 2] = zRand

    xyzs[2, 2] = zRand + 1

    with pytest.raises(ValueError):
        sutils.get_zoom(xyzs)


def test_get_zoom_fails_bad_dims_small():
    """Should fail."""
    xyzs = np.zeros((10, 2))

    with pytest.raises(ValueError):
        sutils.get_zoom(xyzs)


def test_get_zoom_fails_bad_dims_big():
    """Should fail."""
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
