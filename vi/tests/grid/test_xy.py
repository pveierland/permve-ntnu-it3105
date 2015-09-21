import vi.grid.xy

from nose.tools import assert_equals

def test_from_string():
    xy = vi.grid.xy.from_string('2,4')
    assert_equals(xy.x, 2)
    assert_equals(xy.y, 4)
