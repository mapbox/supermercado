from supermercado import super_utils as sutils

import numpy as np

import pytest

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



