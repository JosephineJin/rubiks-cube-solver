"""
Random scramble generator.
"""

from __future__ import annotations
import random
from typing import List
from .cube_state import CubeState
from .move_generator import MOVE_NAMES, apply_move


def random_scramble(length: int = 20, forbid_redundant: bool = True) -> List[str]:
    """Generate a random scramble as a move sequence."""
    from ..utils.move_pruning import is_redundant

    moves: List[str] = []
    while len(moves) < length:
        m = random.choice(MOVE_NAMES)
        if forbid_redundant and moves:
            if is_redundant(moves[-1], m):
                continue
        moves.append(m)
    return moves


def apply_random_scramble(state: CubeState, length: int = 20) -> List[str]:
    """Scramble the cube in-place and return the scramble sequence."""
    sequence = random_scramble(length)
    for m in sequence:
        apply_move(state, m)
    return sequence
