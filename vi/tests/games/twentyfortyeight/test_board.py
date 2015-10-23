from nose.tools import assert_equals

from vi.games.twentyfortyeight import Board
from vi.search.grid import Action

def test_value_conversions():
    for exponent in range(1, 16):
        value     = 2 ** exponent
        converted = Board.value_from_raw(Board.value_to_raw(value))
        assert_equals(value, converted)

def test_value_zero_conversions():
    assert_equals(0, Board.value_from_raw(0))
    assert_equals(0, Board.value_to_raw(0))

def test_move_up_empty():
    initial_state = Board.from_matrix([
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_up).to_matrix()
    assert_equals(result, [
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_up_first_equal():
    initial_state = Board.from_matrix([
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_up).to_matrix()
    assert_equals(result, [
        [ 4, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_up_first_equal_with_follower():
    initial_state = Board.from_matrix([
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_up).to_matrix()
    assert_equals(result, [
        [ 4, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_up_middle_equal():
    initial_state = Board.from_matrix([
        [ 0, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_up).to_matrix()
    assert_equals(result, [
        [ 4, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_up_double_equal():
    initial_state = Board.from_matrix([
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_up).to_matrix()
    assert_equals(result, [
        [ 4, 0, 0, 0 ],
        [ 4, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_up_double_different_equal():
    initial_state = Board.from_matrix([
        [ 4, 0, 0, 0 ],
        [ 4, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_up).to_matrix()
    assert_equals(result, [
        [ 8, 0, 0, 0 ],
        [ 4, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_up_multiple_columns():
    initial_state = Board.from_matrix([
        [ 0, 8, 2, 4 ],
        [ 0, 8, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_up).to_matrix()
    assert_equals(result, [
        [ 0, 16, 2, 4 ],
        [ 0,  0, 0, 0 ],
        [ 0,  0, 0, 0 ],
        [ 0,  0, 0, 0 ] ])

def test_move_up_multiple_opposite():
    initial_state = Board.from_matrix([
        [ 0, 0, 0,  0 ],
        [ 0, 0, 0,  0 ],
        [ 0, 0, 0,  0 ],
        [ 2, 4, 8, 16 ] ])

    result = initial_state.move(Action.move_up).to_matrix()
    assert_equals(result, [
        [ 2, 4, 8, 16 ],
        [ 0, 0, 0,  0 ],
        [ 0, 0, 0,  0 ],
        [ 0, 0, 0,  0 ] ])

#def test_move_down_empty():
#    initial_state = Board.from_matrix([
#        [ 0, 0, 0, 0 ],
#        [ 0, 0, 0, 0 ],
#        [ 0, 0, 0, 0 ],
#        [ 0, 0, 0, 0 ] ])
#
#    result = initial_state.move(Action.move_down).to_matrix()
#    assert_equals(result, [
#        [ 0, 0, 0, 0 ],
#        [ 0, 0, 0, 0 ],
#        [ 0, 0, 0, 0 ],
#        [ 0, 0, 0, 0 ] ])
#
#def test_move_down_first_equal():
#    initial_state = Board.from_matrix([
#        [ 0, 0, 0, 0 ],
#        [ 0, 0, 0, 0 ],
#        [ 2, 0, 0, 0 ],
#        [ 2, 0, 0, 0 ] ])
#
#    result = initial_state.move(Action.move_down).to_matrix()
#    assert_equals(result, [
#        [ 0, 0, 0, 0 ],
#        [ 0, 0, 0, 0 ],
#        [ 0, 0, 0, 0 ],
#        [ 4, 0, 0, 0 ] ])
#
#def test_move_down_first_equal_with_follower():
#    initial_state = Board.from_matrix([
#        [ 0, 0, 0, 0 ],
#        [ 2, 0, 0, 0 ],
#        [ 2, 0, 0, 0 ],
#        [ 2, 0, 0, 0 ] ])
#
#    result = initial_state.move(Action.move_down).to_matrix()
#    assert_equals(result, [
#        [ 0, 0, 0, 0 ],
#        [ 0, 0, 0, 0 ],
#        [ 2, 0, 0, 0 ],
#        [ 4, 0, 0, 0 ] ])
#
#def test_move_down_middle_equal():
#    initial_state = Board.from_matrix([
#        [ 0, 0, 0, 0 ],
#        [ 2, 0, 0, 0 ],
#        [ 2, 0, 0, 0 ],
#        [ 0, 0, 0, 0 ] ])
#
#    result = initial_state.move(Action.move_down).to_matrix()
#    assert_equals(result, [
#        [ 0, 0, 0, 0 ],
#        [ 0, 0, 0, 0 ],
#        [ 0, 0, 0, 0 ],
#        [ 4, 0, 0, 0 ] ])
#
#def test_move_down_double_equal():
#    initial_state = Board.from_matrix([
#        [ 2, 0, 0, 0 ],
#        [ 2, 0, 0, 0 ],
#        [ 2, 0, 0, 0 ],
#        [ 2, 0, 0, 0 ] ])
#
#    result = initial_state.move(Action.move_down).to_matrix()
#    assert_equals(result, [
#        [ 0, 0, 0, 0 ],
#        [ 0, 0, 0, 0 ],
#        [ 4, 0, 0, 0 ],
#        [ 4, 0, 0, 0 ] ])
#
#def test_move_down_double_different_equal():
#    initial_state = Board.from_matrix([
#        [ 2, 0, 0, 0 ],
#        [ 2, 0, 0, 0 ],
#        [ 4, 0, 0, 0 ],
#        [ 4, 0, 0, 0 ] ])
#
#    result = initial_state.move(Action.move_down).to_matrix()
#    assert_equals(result, [
#        [ 0, 0, 0, 0 ],
#        [ 0, 0, 0, 0 ],
#        [ 4, 0, 0, 0 ],
#        [ 8, 0, 0, 0 ] ])
#
#def test_move_down_multiple_columns():
#    initial_state = Board.from_matrix([
#        [ 0, 0, 0, 0 ],
#        [ 0, 0, 0, 0 ],
#        [ 0, 8, 0, 0 ],
#        [ 0, 8, 2, 4 ] ])
#
#    result = initial_state.move(Action.move_down).to_matrix()
#    assert_equals(result, [
#        [ 0,  0, 0, 0 ],
#        [ 0,  0, 0, 0 ],
#        [ 0,  0, 0, 0 ],
#        [ 0, 16, 2, 4 ] ])
#
#def test_move_down_multiple_opposite():
#    initial_state = Board.from_matrix([
#        [ 2, 4, 8, 16 ],
#        [ 0, 0, 0,  0 ],
#        [ 0, 0, 0,  0 ],
#        [ 0, 0, 0,  0 ] ])
#
#    result = initial_state.move(Action.move_down).to_matrix()
#    assert_equals(result, [
#        [ 0, 0, 0,  0 ],
#        [ 0, 0, 0,  0 ],
#        [ 0, 0, 0,  0 ],
#        [ 2, 4, 8, 16 ] ])

def test_move_left_empty():
    initial_state = Board.from_matrix([
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_left).to_matrix()
    assert_equals(result, [
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_left_first_equal():
    initial_state = Board.from_matrix([
        [ 2, 2, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_left).to_matrix()
    assert_equals(result, [
        [ 4, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_left_first_equal_with_follower():
    initial_state = Board.from_matrix([
        [ 2, 2, 2, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_left).to_matrix()
    assert_equals(result, [
        [ 4, 2, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_left_middle_equal():
    initial_state = Board.from_matrix([
        [ 0, 2, 2, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_left).to_matrix()
    assert_equals(result, [
        [ 4, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_left_double_equal():
    initial_state = Board.from_matrix([
        [ 2, 2, 2, 2 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_left).to_matrix()
    assert_equals(result, [
        [ 4, 4, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_left_double_different_equal():
    initial_state = Board.from_matrix([
        [ 2, 2, 4, 4 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_left).to_matrix()
    assert_equals(result, [
        [ 4, 8, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_left_multiple_columns():
    initial_state = Board.from_matrix([
        [ 0, 0, 0, 0 ],
        [ 8, 8, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 4, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_left).to_matrix()
    assert_equals(result, [
        [  0, 0, 0, 0 ],
        [ 16, 0, 0, 0 ],
        [  2, 0, 0, 0 ],
        [  4, 0, 0, 0 ] ])

def test_move_left_multiple_opposite():
    initial_state = Board.from_matrix([
        [ 0, 0, 0,  2 ],
        [ 0, 0, 0,  4 ],
        [ 0, 0, 0,  8 ],
        [ 0, 0, 0, 16 ] ])

    result = initial_state.move(Action.move_left).to_matrix()
    assert_equals(result, [
        [  2, 0, 0, 0 ],
        [  4, 0, 0, 0 ],
        [  8, 0, 0, 0 ],
        [ 16, 0, 0, 0 ] ])

def test_move_right_empty():
    initial_state = Board.from_matrix([
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_right).to_matrix()
    assert_equals(result, [
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_right_first_equal():
    initial_state = Board.from_matrix([
        [ 0, 0, 2, 2 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_right).to_matrix()
    assert_equals(result, [
        [ 0, 0, 0, 4 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_right_first_equal_with_follower():
    initial_state = Board.from_matrix([
        [ 0, 2, 2, 2 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_right).to_matrix()
    assert_equals(result, [
        [ 0, 0, 2, 4 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_right_middle_equal():
    initial_state = Board.from_matrix([
        [ 0, 2, 2, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_right).to_matrix()
    assert_equals(result, [
        [ 0, 0, 0, 4 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_right_double_equal():
    initial_state = Board.from_matrix([
        [ 2, 2, 2, 2 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_right).to_matrix()
    assert_equals(result, [
        [ 0, 0, 4, 4 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_right_double_different_equal():
    initial_state = Board.from_matrix([
        [ 4, 4, 2, 2 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_right).to_matrix()
    assert_equals(result, [
        [ 0, 0, 8, 4 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_right_multiple_columns():
    initial_state = Board.from_matrix([
        [ 0, 0, 0, 0 ],
        [ 0, 0, 8, 8 ],
        [ 0, 0, 0, 2 ],
        [ 0, 0, 0, 4 ] ])

    result = initial_state.move(Action.move_right).to_matrix()
    assert_equals(result, [
        [ 0, 0, 0,  0 ],
        [ 0, 0, 0, 16 ],
        [ 0, 0, 0,  2 ],
        [ 0, 0, 0,  4 ] ])

def test_move_right_multiple_opposite():
    initial_state = Board.from_matrix([
        [  2, 0, 0, 0 ],
        [  4, 0, 0, 0 ],
        [  8, 0, 0, 0 ],
        [ 16, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_right).to_matrix()
    assert_equals(result, [
        [ 0, 0, 0,  2 ],
        [ 0, 0, 0,  4 ],
        [ 0, 0, 0,  8 ],
        [ 0, 0, 0, 16 ] ])
