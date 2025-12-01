"""
Edge orientation-ish pattern database.

We build a small PDB over a coarse pattern:

    key = which non-center stickers on U and D faces are incorrect,
          encoded as a 16-bit mask (8 positions on U, 8 on D).

During precomputation, we BFS from the solved cube up to some depth
and store the minimum number of moves needed to reach each pattern.

At solve time, we look up the pattern's cost in the table. If there is
no table (or the pattern wasn't seen), we fall back to a simple
misplaced-sticker count, scaled down to stay admissible-ish.
"""

from __future__ import annotations
import os
from typing import Tuple
from .pattern_database import PatternDatabase
from ..cube.cube_state import CubeState


def _default_db_path() -> str:
    # src/heuristics/edge_orient_pdb.py
    here = os.path.dirname(__file__)
    # project_root = .../src/..
    project_root = os.path.abspath(os.path.join(here, "..", ".."))
    return os.path.join(project_root, "data", "pattern_dbs", "edge_orient_pdb.pkl")


class EdgeOrientPDB(PatternDatabase):
    def __init__(self, db_path: str | None = None):
        if db_path is None:
            db_path = _default_db_path()
        super().__init__(db_path=db_path)

    def encode(self, state: CubeState) -> int:
        """
        Encode pattern as a 16-bit mask:

        bits 0–7  : non-center stickers on U (row-major, skipping center)
        bits 8–15 : non-center stickers on D

        A bit is 1 if the sticker != center color for that face.
        """
        faces = state.faces
        mask = 0
        bit_index = 0

        for face_name in ("U", "D"):
            face = faces[face_name]
            center = face[4]
            for pos in range(9):
                if pos == 4:
                    continue  # skip center
                if face[pos] != center:
                    mask |= (1 << bit_index)
                bit_index += 1

        return mask

    def h(self, state: CubeState) -> int:
        """
        Lookup heuristic:

        - If a PDB table is loaded and contains this pattern key, return that.
        - Otherwise, use a simple fallback:
            popcount(mask) // 4

          (Very conservative so it's almost certainly admissible.)
        """
        key = self.encode(state)

        # If we have a PDB loaded and it has this pattern, use it.
        if self.table:
            if key in self.table:
                return self.table[key]
            # If not seen during BFS, we don't know the true cost, so returning 0
            # is always safe (admissible). But we can also fall back to the
            # cheap heuristic for a bit more guidance while still being
            # conservative.
            # Comment one of these out depending on how conservative you want:
            # return 0
            # Fallback:
            return self._fallback_heuristic_from_mask(key)

        # No table loaded at all: just use the cheap heuristic.
        return self._fallback_heuristic_from_mask(key)

    @staticmethod
    def _fallback_heuristic_from_mask(mask: int) -> int:
        """Cheap admissible-ish fallback from mask alone."""
        misplaced = bin(mask).count("1")
        # Each move can potentially fix several stickers, so divide.
        return misplaced // 4
