import numpy as np
from reversi.logic import (
    _increment_search,
    execute_action,
    init_board,
    is_legal_action,
    obtain_legal_actions,
)
from reversi.models import Board, Direction, Disk, Position, Square


def test_init_board():
    config = np.array(
        [
            [0, 0, 0, 0],
            [0, -1, 1, 0],
            [0, 1, -1, 0],
            [0, 0, 0, 0],
        ],
        np.int8,
    )
    assert Board(config) == init_board(4)


def test_is_legal_action():
    board = init_board(4)
    assert not is_legal_action(board, Disk.LIGHT, Position(0, 0))
    assert not is_legal_action(board, Disk.LIGHT, Position(0, 1))
    assert is_legal_action(board, Disk.LIGHT, Position(0, 2))


def test_increment_search():
    config = np.array(
        [
            [1, -1, -1, 0],
            [0, 1, -1, 0],
            [0, 0, 0, 0],
            [0, 1, -1, 0],
        ]
    )
    board = Board(config)
    assert _increment_search(board, Disk.DARK, Position(3, 1), Direction(0, -1)) == (
        True,
        Position(3, 1),
    )
    assert _increment_search(board, Disk.DARK, Position(3, 2), Direction(0, -1)) == (
        True,
        Position(3, 1),
    )
    assert _increment_search(board, Disk.DARK, Position(3, 3), Direction(0, -1)) == (
        False,
        None,
    )
    assert _increment_search(board, Disk.DARK, Position(0, 1), Direction(0, -1)) == (
        True,
        Position(0, 0),
    )
    assert _increment_search(board, Disk.DARK, Position(0, 2), Direction(0, -1)) == (
        True,
        Position(0, 0),
    )
    assert _increment_search(board, Disk.DARK, Position(0, 3), Direction(0, -1)) == (
        False,
        None,
    )


def test_obtain_legal_actions():
    board = init_board(4)
    assert obtain_legal_actions(board, Disk.LIGHT) == frozenset(
        [Position(0, 2), Position(1, 3), Position(2, 0), Position(3, 1)]
    )
    board = Board(np.zeros((4, 4), dtype=np.int8))
    assert obtain_legal_actions(board, Disk.LIGHT) == frozenset()


def test_execute_action():
    board = init_board(4)
    new_board = execute_action(board, Disk.LIGHT, Position(1, 3))
    config = np.array(
        [
            [0, 0, 0, 0],
            [0, -1, -1, -1],
            [0, 1, -1, 0],
            [0, 0, 0, 0],
        ]
    )
    assert new_board == Board(config)

    config = np.array(
        [
            [0, -1, -1, 1],
            [-1, -1, -1, 1],
            [1, -1, -1, 1],
            [0, -1, -1, 1],
        ],
        dtype=np.int8,
    )
    board = Board(config)
    new_board = execute_action(board, Disk.DARK, Position(0, 0))
    after_config = np.array(
        [
            [1, 1, 1, 1],
            [1, 1, -1, 1],
            [1, -1, 1, 1],
            [0, -1, -1, 1],
        ],
        dtype=np.int8,
    )
    assert new_board == Board(after_config)
