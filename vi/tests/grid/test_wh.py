import vi.grid.wh

from nose.tools import assert_equals

def test_from_string():
    wh = vi.grid.wh.from_string('2,4')
    assert_equals(wh.w, 2)
    assert_equals(wh.h, 4)
