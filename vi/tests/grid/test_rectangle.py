from vi.grid import Coordinate, Rectangle

from nose.tools import assert_equals

#o o o o o o
#o o o o o o
#o o o x x o
#o o o x x o
#o o o x x o
#o o o x x o
#o o o o o o

def test_distance_to_coordinate():
    rectangle = Rectangle(3, 2, 2, 4)

    assert_equals(rectangle.distance_to_coordinate(Coordinate(3, 1)), (0,  1))
    assert_equals(rectangle.distance_to_coordinate(Coordinate(3, 2)), (0,  0))
    assert_equals(rectangle.distance_to_coordinate(Coordinate(3, 3)), (0, -1))
    assert_equals(rectangle.distance_to_coordinate(Coordinate(3, 4)), (0, -1))
    assert_equals(rectangle.distance_to_coordinate(Coordinate(3, 5)), (0,  0))
    assert_equals(rectangle.distance_to_coordinate(Coordinate(3, 6)), (0,  1))

def test_intersects_coordinate():
    rectangle = Rectangle(3, 2, 2, 4)

    assert rectangle.intersects_coordinate(Coordinate(3, 2))
    assert rectangle.intersects_coordinate(Coordinate(3, 3))
    assert rectangle.intersects_coordinate(Coordinate(3, 4))
    assert rectangle.intersects_coordinate(Coordinate(3, 5))
    
    assert rectangle.intersects_coordinate(Coordinate(4, 2))
    assert rectangle.intersects_coordinate(Coordinate(4, 3))
    assert rectangle.intersects_coordinate(Coordinate(4, 4))
    assert rectangle.intersects_coordinate(Coordinate(4, 5))

    assert not rectangle.intersects_coordinate(Coordinate(2, 1))
    assert not rectangle.intersects_coordinate(Coordinate(2, 2))
    assert not rectangle.intersects_coordinate(Coordinate(2, 3))
    assert not rectangle.intersects_coordinate(Coordinate(2, 4))
    assert not rectangle.intersects_coordinate(Coordinate(2, 5))
    assert not rectangle.intersects_coordinate(Coordinate(2, 6))
    
    assert not rectangle.intersects_coordinate(Coordinate(3, 1))
    assert not rectangle.intersects_coordinate(Coordinate(3, 6))
    
    assert not rectangle.intersects_coordinate(Coordinate(4, 1))
    assert not rectangle.intersects_coordinate(Coordinate(4, 6))
    
    assert not rectangle.intersects_coordinate(Coordinate(5, 1))
    assert not rectangle.intersects_coordinate(Coordinate(5, 2))
    assert not rectangle.intersects_coordinate(Coordinate(5, 3))
    assert not rectangle.intersects_coordinate(Coordinate(5, 4))
    assert not rectangle.intersects_coordinate(Coordinate(5, 5))
    assert not rectangle.intersects_coordinate(Coordinate(5, 6))
