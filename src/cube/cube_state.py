"""
Facelet-based Rubik's Cube representation.

Faces: U, R, F, D, L, B
Each face has 9 stickers indexed as:

0 1 2
3 4 5
6 7 8
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


FACE_ORDER = ["U", "R", "F", "D", "L", "B"]


@dataclass
class CubeState:
    """Facelet-based cube.

    `faces` is a dict mapping face letter to a list of 9 stickers.
    Stickers are just strings (e.g. 'U', 'R', ...).
    """

    faces: Dict[str, List[str]]

    @classmethod
    def solved(cls) -> "CubeState":
        faces = {f: [f] * 9 for f in FACE_ORDER}
        return cls(faces)

    def copy(self) -> "CubeState":
        return CubeState({f: stickers[:] for f, stickers in self.faces.items()})

    def is_solved(self) -> bool:
        return all(all(s == face[0] for s in face) for face in self.faces.values())

    def to_string(self) -> str:
        """Flatten to a 54-character string: U(9) R(9) F(9) D(9) L(9) B(9)."""
        return "".join("".join(self.faces[f]) for f in FACE_ORDER)

    @classmethod
    def from_string(cls, s: str) -> "CubeState":
        assert len(s) == 54
        faces: Dict[str, List[str]] = {}
        i = 0
        for f in FACE_ORDER:
            faces[f] = list(s[i : i + 9])
            i += 9
        return cls(faces)

    def apply_move(self, move: str) -> None:
        """In-place application of a move string like 'U', 'U2', 'U''."""
        # Lazy import to avoid circular dependency.
        from .move_generator import apply_move

        apply_move(self, move)

    def __hash__(self) -> int:  # to use in sets / dicts
        return hash(self.to_string())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CubeState):
            return False
        return self.faces == other.faces
