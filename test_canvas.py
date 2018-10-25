import pytest
import numpy as np

import atsumaru


def test_canvas_empty():
    """Canvas should have no available slots when created."""
    canvas_size = (10, 12)
    canvas = atsumaru.Canvas(canvas_size)
    
    assert len(canvas.available) == 0


def test_canvas_retrieve():
    """Should be able to retrieve something inserted."""
    canvas_size = (10, 12)
    canvas = atsumaru.Canvas(canvas_size)
    inserted = 1
    
    canvas.insert(inserted, (5, 5))
    retrieved = canvas.get((5, 5))

    assert retrieved == inserted


def test_canvas_availability():
    """When something is inserted it should create available slots."""
    canvas_size = (10, 12)
    canvas = atsumaru.Canvas(canvas_size)
    expected = set([(4, 5), (6, 5), (5, 4), (5, 6)])
    
    canvas.insert(1, (5, 5))

    assert len(canvas.available) == 4
    assert canvas.available == expected


def test_available_at_edge():
    """Things beyond the edge shouldn't be available."""
    canvas_size = (10, 12)
    canvas = atsumaru.Canvas(canvas_size)
    expected = set([(1, 0), (0, 1)])

    canvas.insert(1, (0, 0))

    assert len(canvas.available) == 2
    assert canvas.available == expected


def test_canvas_no_duplicates():
    """Available slots shouldn't be duplicated."""
    canvas_size = (10, 12)
    canvas = atsumaru.Canvas(canvas_size)
    expected = set([(1, 0), (0, 1), (2, 1), (1, 2)])
    
    canvas.insert(1, (0, 0))
    canvas.insert(1, (1, 1))

    assert len(canvas.available) == 4
    assert canvas.available == expected


def test_canvas_fill_available():
    """Inserting should fill available slots."""
    canvas_size = (10, 12)
    canvas = atsumaru.Canvas(canvas_size)
    expected = set([(0, 0), (0, 1), (2, 1), (1, 2), (2, 0)])
    
    canvas.insert(1, (1, 1))
    canvas.insert(1, (1, 0))

    assert len(canvas.available) == 5
    assert canvas.available == expected


def test_get_neighbours():
    """Neighbours should be a dict of relative pos and contents."""
    canvas_size = (10, 12)
    canvas = atsumaru.Canvas(canvas_size)
    canvas.insert(1, (1, 1))
    expected_neighbours = {(0, 1): 1}

    neighbours = canvas.get_neighbours((1, 0))

    assert neighbours == expected_neighbours


def test_get_multiple_neighbours():
    """Neighbours should work with multiple neighbours."""
    canvas_size = (8, 9)
    canvas = atsumaru.Canvas(canvas_size)
    canvas.insert(1, (1, 1))
    canvas.insert(2, (2, 0))
    expected_neighbours = {(1, 0): 2,
                            (0, 1): 1,
                            }
    
    neighbours = canvas.get_neighbours((1, 0))

    assert len(neighbours) == 2
    assert neighbours == expected_neighbours

