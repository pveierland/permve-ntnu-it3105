from nose.tools import assert_equals

from vi.games.twentyfortyeight import State
from vi.search.grid import Action

def test_move_up_empty():
    initial_state = State([
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_up).to_list()
    assert_equals(result, [
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_up_first_equal():
    initial_state = State([
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_up).to_list()
    assert_equals(result, [
        [ 4, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_up_first_equal_with_follower():
    initial_state = State([
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_up).to_list()
    assert_equals(result, [
        [ 4, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_up_middle_equal():
    initial_state = State([
        [ 0, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_up).to_list()
    assert_equals(result, [
        [ 4, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_up_double_equal():
    initial_state = State([
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_up).to_list()
    assert_equals(result, [
        [ 4, 0, 0, 0 ],
        [ 4, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_up_double_different_equal():
    initial_state = State([
        [ 4, 0, 0, 0 ],
        [ 4, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_up).to_list()
    assert_equals(result, [
        [ 8, 0, 0, 0 ],
        [ 4, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_up_multiple_columns():
    initial_state = State([
        [ 0, 8, 2, 4 ],
        [ 0, 8, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_up).to_list()
    assert_equals(result, [
        [ 0, 16, 2, 4 ],
        [ 0,  0, 0, 0 ],
        [ 0,  0, 0, 0 ],
        [ 0,  0, 0, 0 ] ])

def test_move_down_empty():
    initial_state = State([
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_down).to_list()
    assert_equals(result, [
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_down_first_equal():
    initial_state = State([
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_down).to_list()
    assert_equals(result, [
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 4, 0, 0, 0 ] ])

def test_move_down_first_equal_with_follower():
    initial_state = State([
        [ 0, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_down).to_list()
    assert_equals(result, [
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 4, 0, 0, 0 ] ])

def test_move_down_middle_equal():
    initial_state = State([
        [ 0, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_down).to_list()
    assert_equals(result, [
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 4, 0, 0, 0 ] ])

def test_move_down_double_equal():
    initial_state = State([
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_down).to_list()
    assert_equals(result, [
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 4, 0, 0, 0 ],
        [ 4, 0, 0, 0 ] ])

def test_move_down_double_different_equal():
    initial_state = State([
        [ 2, 0, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 4, 0, 0, 0 ],
        [ 4, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_down).to_list()
    assert_equals(result, [
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 4, 0, 0, 0 ],
        [ 8, 0, 0, 0 ] ])

def test_move_down_multiple_columns():
    initial_state = State([
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 8, 0, 0 ],
        [ 0, 8, 2, 4 ] ])

    result = initial_state.move(Action.move_down).to_list()
    assert_equals(result, [
        [ 0,  0, 0, 0 ],
        [ 0,  0, 0, 0 ],
        [ 0,  0, 0, 0 ],
        [ 0, 16, 2, 4 ] ])

def test_move_left_empty():
    initial_state = State([
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_left).to_list()
    assert_equals(result, [
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_left_first_equal():
    initial_state = State([
        [ 2, 2, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_left).to_list()
    assert_equals(result, [
        [ 4, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_left_first_equal_with_follower():
    initial_state = State([
        [ 2, 2, 2, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_left).to_list()
    assert_equals(result, [
        [ 4, 2, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_left_middle_equal():
    initial_state = State([
        [ 0, 2, 2, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_left).to_list()
    assert_equals(result, [
        [ 4, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_left_double_equal():
    initial_state = State([
        [ 2, 2, 2, 2 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_left).to_list()
    assert_equals(result, [
        [ 4, 4, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_left_double_different_equal():
    initial_state = State([
        [ 2, 2, 4, 4 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_left).to_list()
    assert_equals(result, [
        [ 4, 8, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_left_multiple_columns():
    initial_state = State([
        [ 0, 0, 0, 0 ],
        [ 8, 8, 0, 0 ],
        [ 2, 0, 0, 0 ],
        [ 4, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_left).to_list()
    assert_equals(result, [
        [  0, 0, 0, 0 ],
        [ 16, 0, 0, 0 ],
        [  2, 0, 0, 0 ],
        [  4, 0, 0, 0 ] ])

def test_move_right_empty():
    initial_state = State([
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_right).to_list()
    assert_equals(result, [
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_right_first_equal():
    initial_state = State([
        [ 0, 0, 2, 2 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_right).to_list()
    assert_equals(result, [
        [ 0, 0, 0, 4 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_right_first_equal_with_follower():
    initial_state = State([
        [ 0, 2, 2, 2 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_right).to_list()
    assert_equals(result, [
        [ 0, 0, 2, 4 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_right_middle_equal():
    initial_state = State([
        [ 0, 2, 2, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_right).to_list()
    assert_equals(result, [
        [ 0, 0, 0, 4 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_right_double_equal():
    initial_state = State([
        [ 2, 2, 2, 2 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_right).to_list()
    assert_equals(result, [
        [ 0, 0, 4, 4 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_right_double_different_equal():
    initial_state = State([
        [ 4, 4, 2, 2 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

    result = initial_state.move(Action.move_right).to_list()
    assert_equals(result, [
        [ 0, 0, 8, 4 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ],
        [ 0, 0, 0, 0 ] ])

def test_move_right_multiple_columns():
    initial_state = State([
        [ 0, 0, 0, 0 ],
        [ 0, 0, 8, 8 ],
        [ 0, 0, 0, 2 ],
        [ 0, 0, 0, 4 ] ])

    result = initial_state.move(Action.move_right).to_list()
    assert_equals(result, [
        [ 0, 0, 0,  0 ],
        [ 0, 0, 0, 16 ],
        [ 0, 0, 0,  2 ],
        [ 0, 0, 0,  4 ] ])
