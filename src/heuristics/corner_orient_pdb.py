"""
Corner orientation heuristic shell.

NOTE: For now this is a very simple, admissible but weak heuristic:
it just counts how many stickers on the U and D faces are not
equal to their center colors, divided by 8.
"""

from __future__ import annotations
from typing import Tuple
from .pattern_database import PatternDatabase
from ..cube.cube_state import CubeState


class CornerOrientPDB(PatternDatabase):
    def encode(self, state: CubeState) -> Tuple:
        # For placeholder, just use the faces string.
        return (state.to_string(),)

    def h(self, state: CubeState) -> int:
        faces = state.faces
        count = 0
        for face_name in ["U", "D"]:
            face = faces[face_name]
            center = face[4]
            count += sum(1 for i in range(9) if i != 4 and face[i] != center)
        # Very conservative scaling to keep admissible-ish
        return count // 8
