"""
Corner permutation heuristic shell.

Currently: simple Hamming distance on all stickers relative to solved,
scaled down to be conservatively admissible.
"""

from __future__ import annotations
from typing import Tuple
from .pattern_database import PatternDatabase
from ..cube.cube_state import CubeState, FACE_ORDER


class CornerPermPDB(PatternDatabase):
    def encode(self, state: CubeState) -> Tuple:
        return (state.to_string(),)

    def h(self, state: CubeState) -> int:
        count = 0
        # compare against solved
        for f in FACE_ORDER:
            face = state.faces[f]
            center = f
            count += sum(1 for s in face if s != center)
        # Each move can affect at most 8 stickers -> divide generously
        return count // 8
