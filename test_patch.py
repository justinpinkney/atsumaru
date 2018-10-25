import atsumaru

import numpy as np

def test_create_image_patch():
    input_data = np.zeros((10, 10))
    im = atsumaru.Patch(input_data)
    np.testing.assert_array_equal(input_data, im.data)

