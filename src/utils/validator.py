"""
Solution validation utilities.
"""

from __future__ import annotations
from typing import List
from ..cube.cube_state import CubeState
from ..cube.move_generator import MOVE_NAMES, apply_move


def is_valid_move_sequence(moves: List[str]) -> bool:
    return all(m in MOVE_NAMES for m in moves)


def validate_solution(start: CubeState, moves: List[str]) -> bool:
    if not is_valid_move_sequence(moves):
        return False
    state = start.copy()
    for m in moves:
        apply_move(state, m)
    return state.is_solved()
