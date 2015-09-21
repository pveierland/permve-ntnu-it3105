import vi.grid.xywh

from nose.tools import assert_equals

def test_from_string():
    xywh = vi.grid.xywh.from_string('1,2,3,4')
    assert_equals(xywh.x, 1)
    assert_equals(xywh.y, 2)
    assert_equals(xywh.width, 3)
    assert_equals(xywh.height, 4)
