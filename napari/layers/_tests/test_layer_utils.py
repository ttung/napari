import numpy as np
import pytest
from dask import array as da

from ..layer_utils import (
    calc_data_range,
    increment_unnamed_colormap,
    segment_normal,
)


data_dask = da.random.random(
    size=(100_000, 1000, 1000), chunks=(1, 1000, 1000)
)


def test_calc_data_range():
    # all zeros should return [0, 1] by default
    data = np.zeros((10, 10))
    clim = calc_data_range(data)
    assert np.all(clim == [0, 1])

    # all ones should return [0, 1] by default
    data = np.ones((10, 10))
    clim = calc_data_range(data)
    assert np.all(clim == [0, 1])

    # return min and max
    data = np.random.random((10, 15))
    data[0, 0] = 0
    data[0, 1] = 2
    clim = calc_data_range(data)
    assert np.all(clim == [0, 2])

    # return min and max
    data = np.random.random((6, 10, 15))
    data[0, 0, 0] = 0
    data[0, 0, 1] = 2
    clim = calc_data_range(data)
    assert np.all(clim == [0, 2])

    # Try large data
    data = np.zeros((1000, 2000))
    data[0, 0] = 0
    data[0, 1] = 2
    clim = calc_data_range(data)
    assert np.all(clim == [0, 2])

    # Try large data mutlidimensional
    data = np.zeros((3, 1000, 1000))
    data[0, 0, 0] = 0
    data[0, 0, 1] = 2
    clim = calc_data_range(data)
    assert np.all(clim == [0, 2])


def test_calc_data_fast_uint8():
    data = da.random.randint(
        0,
        100,
        size=(100_000, 1000, 1000),
        chunks=(1, 1000, 1000),
        dtype=np.uint8,
    )
    assert calc_data_range(data) == [0, 255]


@pytest.mark.timeout(2)
def test_calc_data_range_fast_big():
    val = calc_data_range(data_dask)
    assert len(val) > 0


def test_segment_normal_2d():
    a = np.array([1, 1])
    b = np.array([1, 10])

    unit_norm = segment_normal(a, b)
    assert np.all(unit_norm == np.array([1, 0]))


def test_segment_normal_3d():
    a = np.array([1, 1, 0])
    b = np.array([1, 10, 0])
    p = np.array([1, 0, 0])

    unit_norm = segment_normal(a, b, p)
    assert np.all(unit_norm == np.array([0, 0, -1]))


def test_increment_unnamed_colormap():
    # test that unnamed colormaps are incremented
    names = [
        '[unnamed colormap 0',
        'existing_colormap',
        'perceptually_uniform',
        '[unnamed colormap 1]',
    ]
    name = '[unnamed colormap]'
    assert increment_unnamed_colormap(name, names) == '[unnamed colormap 2]'

    # test that named colormaps are not incremented
    named_colormap = 'perfect_colormap'
    assert increment_unnamed_colormap(named_colormap, names) == named_colormap
