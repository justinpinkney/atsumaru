import pytest
import numpy as np

import atsumaru

def test_create_image_patch():
    input_data = np.zeros((10, 10))
    im = atsumaru.Patch(input_data)
    np.testing.assert_array_equal(input_data, im.data)


def test_canvas_empty():
    canvas_size = (10, 12)
    canvas = atsumaru.Canvas(canvas_size)
    
    assert len(canvas.available) == 0


def test_canvas_availability():
    canvas_size = (10, 12)
    canvas = atsumaru.Canvas(canvas_size)
    
    patch = atsumaru.Patch([])
    canvas.insert(patch, (0, 0))
    expected = set([(1, 0), (0, 1)])

    assert len(canvas.available) == 2
    assert canvas.available == expected

    canvas.insert(patch, (5, 5))
    expected.update([(4, 5), (6, 5), (5, 4), (5, 6)])

    assert len(canvas.available) == 6
    assert canvas.available == expected


def test_canvas_no_duplicates():
    canvas_size = (10, 12)
    canvas = atsumaru.Canvas(canvas_size)
    
    patch = atsumaru.Patch([])
    canvas.insert(patch, (0, 0))
    canvas.insert(patch, (1, 1))
    expected = set([(1, 0), (0, 1), (2, 1), (1, 2)])

    assert len(canvas.available) == 4
    assert canvas.available == expected


def test_canvas_fill_available():
    canvas_size = (10, 12)
    canvas = atsumaru.Canvas(canvas_size)
    
    patch = atsumaru.Patch([])
    canvas.insert(patch, (1, 1))
    canvas.insert(patch, (1, 0))
    expected = set([(0, 0), (0, 1), (2, 1), (1, 2), (2, 0)])

    assert len(canvas.available) == 5
    assert canvas.available == expected
