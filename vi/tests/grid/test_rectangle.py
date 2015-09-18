import vi.grid.rectangle

from nose.tools import assert_equals

def test_from_string():
    rectangle = vi.grid.rectangle.from_string('1,2,3,4')
    assert_equals(rectangle.x, 1)
    assert_equals(rectangle.y, 2)
    assert_equals(rectangle.width, 3)
    assert_equals(rectangle.height, 4)
