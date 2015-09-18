import vi.grid.coordinate

from nose.tools import assert_equals

def test_from_string():
    coordinate = vi.grid.coordinate.from_string('2,4')
    assert_equals(coordinate.x, 2)
    assert_equals(coordinate.y, 4)
