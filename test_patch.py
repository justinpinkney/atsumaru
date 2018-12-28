import atsumaru

import numpy as np

import math

def test_create_image_patch():
    """The data returned should be the same as input."""
    input_data = np.zeros((10, 10))

    im = atsumaru.Patch(input_data)

    np.testing.assert_array_equal(input_data, im.data)


def test_parameter():
    """Rotation parameter should affect data."""
    input_data = np.array([[0, 1], [2, 3]])
    patch = atsumaru.Patch(input_data)

    patch.orientation = 'RIGHT'

    expected_data = np.array([[2, 0], [3, 1]])
    np.testing.assert_array_equal(expected_data, patch.data)

    patch.orientation = 'UP'
    np.testing.assert_array_equal(input_data, patch.data)
