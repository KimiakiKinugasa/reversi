"""reversi logic

fundamental elements and logics of reversi
"""
from __future__ import annotations

from typing import FrozenSet, Optional, Tuple

import numpy as np

from .models import _DIRECTIONS, Board, Direction, Disk, Position, Square


def init_board(length: int):
    """initialize board

    Args:
        length (int): length of board
    """
    config = np.zeros((length, length), dtype=np.int8)
    config[length // 2][length // 2] = Square.LIGHT
    config[length // 2 - 1][length // 2 - 1] = Square.LIGHT
    config[length // 2][length // 2 - 1] = Square.DARK
    config[length // 2 - 1][length // 2] = Square.DARK
    return Board(config)


def obtain_legal_actions(board: Board, disk: Disk) -> FrozenSet[Position]:
    """obtain legal actions

    Args:
        board (Board): 盤の状態
        disk (Disk): 置きたい石

    Returns:
        FrozenSet[Position]: legal actions
    """
    return frozenset(
        filter(
            lambda position: is_legal_action(board, disk, position),
            [
                Position(row, col)
                for row in range(board.length)
                for col in range(board.length)
            ],
        )
    )


def is_legal_action(board: Board, disk: Disk, position: Position) -> bool:
    """legal actionか

    Args:
        board (Board): 盤の状態
        disk (Disk): 置きたい石
        position (Position): 置きたい位置

    Returns:
        bool: True if legal, False if illegal
    """
    if board[position] != Square.NULL:
        return False
    # 周囲8マスにdiskの逆がなければfalse
    # 周囲8マスにdiskの逆がある場合，その方向に進んで，NULLにならずにdiskがあればTrue
    for direction in _DIRECTIONS:
        adjacent_position = position + direction
        # 隣の位置がマスをはみ出すか隣の位置のマスの色がdiskの逆でないないなら
        if (
            not (
                Position(0, 0)
                <= adjacent_position
                < Position(board.length, board.length)
            )
            or board[adjacent_position] != disk.reverse()
        ):
            continue
        legal, _ = _increment_search(board, disk, adjacent_position, direction)
        if legal:
            return True
    return False


def _increment_search(
    board: Board, disk: Disk, position: Position, direction: Direction
) -> Tuple[bool, Optional[Position]]:
    """diskと同じ色の位置を探す

    positionからdirectionの方向に進み，空マスに出会わず，diskと同じ色のマスに到達できるか．
    到達できたら，その位置も返す

    Args:
        board (Board): 盤の状態
        disk (Disk): 探す色
        position (Position): 調べるマス
        direction (Direction): 探す方向

    Returns:
        Tuple[bool, Optional[Position]]: diskのマスに到達できたかの真偽値と到達した位置
    """
    if not Position(0, 0) <= position < Position(board.length, board.length):
        return False, None
    if board[position] == Square.NULL:
        return False, None
    if board[position] == disk:
        return True, position
    return _increment_search(
        board,
        disk,
        position + direction,
        direction,
    )


def execute_action(board: Board, disk: Disk, position: Position) -> Board:
    """execute action and return new state board

    positionは必ずlegalなものを使うこと．この関数ではlegalかのチェックはしない

    Args:
        board (Board): 盤
        disk (Disk): 石の色
        position (Position): 石を置く場所
    Returns:
        Board: 石が置かれた新しい状態の盤
    """
    flip_position_list = [position]
    for direction in _DIRECTIONS:
        adjacent_position = position + direction
        # 隣の位置がマスをはみ出すか隣の位置のマスの色がdiskの逆でないないなら
        if (
            not (
                Position(0, 0)
                <= adjacent_position
                < Position(board.length, board.length)
            )
            or board[adjacent_position] != disk.reverse()
        ):
            continue
        legal, end_position = _increment_search(
            board, disk, adjacent_position, direction
        )
        while legal and adjacent_position != end_position:
            flip_position_list.append(adjacent_position)
            adjacent_position = adjacent_position + direction

    # flip_position_listが1なら一枚もひっくり返らないのでlegal actionではない
    # 関数呼び出し側がちゃんとlegal actionとなるように注意する
    assert len(flip_position_list) > 1
    config = board.config.copy()
    for position in flip_position_list:
        config[position] = disk
    return Board(config)


def count_disk(board: Board, disk: Disk) -> int:
    """count disk

    Args:
        board (Board): 盤の状態
        disk (Disk): 数えたい石の種類

    Returns:
        int: 数えたい石の数
    """
    return np.sum(board.config == disk)
