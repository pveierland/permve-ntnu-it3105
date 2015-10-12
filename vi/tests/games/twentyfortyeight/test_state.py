from nose.tools import assert_equals

from vi.games.twentyfortyeight import State
from vi.search.grid import Action

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
