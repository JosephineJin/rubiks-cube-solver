"""
Move definitions for the facelet-based cube.

We implement 6 base face turns (U, R, F, D, L, B) clockwise,
and derive U2, U', etc. by composition.
"""

from __future__ import annotations
from typing import Dict, Callable, List
from .cube_state import CubeState

# Move names in quarter-turn metric
MOVE_NAMES: List[str] = [
    "U", "U2", "U'",
    "R", "R2", "R'",
    "F", "F2", "F'",
    "D", "D2", "D'",
    "L", "L2", "L'",
    "B", "B2", "B'",
]

# Helpers


def _rotate_face_cw(face: List[str]) -> List[str]:
    """Rotate a 3x3 face clockwise."""
    # indices mapping for CW rotation
    return [face[i] for i in [6, 3, 0, 7, 4, 1, 8, 5, 2]]


def _rotate_face_ccw(face: List[str]) -> List[str]:
    """Rotate a 3x3 face counter-clockwise."""
    return [face[i] for i in [2, 5, 8, 1, 4, 7, 0, 3, 6]]


def _rotate_face_180(face: List[str]) -> List[str]:
    """Rotate a 3x3 face 180 degrees."""
    return [face[i] for i in [8, 7, 6, 5, 4, 3, 2, 1, 0]]


# Base moves (clockwise quarter turns)


def _move_U_cw(cube: CubeState) -> None:
    f = cube.faces
    f["U"] = _rotate_face_cw(f["U"])
    # Cycle top rows of F, R, B, L
    F, R, B, L = f["F"], f["R"], f["B"], f["L"]
    tmp = F[0:3]
    F[0:3] = L[0:3]
    L[0:3] = B[0:3]
    B[0:3] = R[0:3]
    R[0:3] = tmp


def _move_D_cw(cube: CubeState) -> None:
    f = cube.faces
    f["D"] = _rotate_face_cw(f["D"])
    F, R, B, L = f["F"], f["R"], f["B"], f["L"]
    tmp = F[6:9]
    F[6:9] = R[6:9]
    R[6:9] = B[6:9]
    B[6:9] = L[6:9]
    L[6:9] = tmp


def _move_R_cw(cube: CubeState) -> None:
    f = cube.faces
    f["R"] = _rotate_face_cw(f["R"])
    U, F, D, B = f["U"], f["F"], f["D"], f["B"]

    tmp = [U[2], U[5], U[8]]
    U[2], U[5], U[8] = F[2], F[5], F[8]
    F[2], F[5], F[8] = D[2], D[5], D[8]
    D[2], D[5], D[8] = B[6], B[3], B[0]
    B[6], B[3], B[0] = tmp


def _move_L_cw(cube: CubeState) -> None:
    f = cube.faces
    f["L"] = _rotate_face_cw(f["L"])
    U, F, D, B = f["U"], f["F"], f["D"], f["B"]

    tmp = [U[0], U[3], U[6]]
    U[0], U[3], U[6] = B[8], B[5], B[2]
    B[8], B[5], B[2] = D[0], D[3], D[6]
    D[0], D[3], D[6] = F[0], F[3], F[6]
    F[0], F[3], F[6] = tmp


def _move_F_cw(cube: CubeState) -> None:
    f = cube.faces
    f["F"] = _rotate_face_cw(f["F"])
    U, R, D, L = f["U"], f["R"], f["D"], f["L"]

    tmp = [U[6], U[7], U[8]]
    U[6], U[7], U[8] = L[8], L[5], L[2]
    L[8], L[5], L[2] = D[2], D[1], D[0]
    D[2], D[1], D[0] = R[0], R[3], R[6]
    R[0], R[3], R[6] = tmp


def _move_B_cw(cube: CubeState) -> None:
    f = cube.faces
    f["B"] = _rotate_face_cw(f["B"])
    U, R, D, L = f["U"], f["R"], f["D"], f["L"]

    tmp = [U[0], U[1], U[2]]
    U[0], U[1], U[2] = R[2], R[5], R[8]
    R[2], R[5], R[8] = D[8], D[7], D[6]
    D[8], D[7], D[6] = L[6], L[3], L[0]
    L[6], L[3], L[0] = tmp


_BASE_CW: Dict[str, Callable[[CubeState], None]] = {
    "U": _move_U_cw,
    "R": _move_R_cw,
    "F": _move_F_cw,
    "D": _move_D_cw,
    "L": _move_L_cw,
    "B": _move_B_cw,
}


def apply_move(cube: CubeState, move: str) -> None:
    """Apply a single move in-place."""
    if move not in MOVE_NAMES:
        raise ValueError(f"Unknown move: {move}")

    base = move[0]
    if base not in _BASE_CW:
        raise ValueError(f"Unknown base move: {base}")

    if len(move) == 1:  # e.g. 'U'
        _BASE_CW[base](cube)
    elif move[1] == "2":  # 'U2'
        _BASE_CW[base](cube)
        _BASE_CW[base](cube)
    elif move[1] == "'":  # "U'"
        # three clockwise turns == one counter-clockwise
        _BASE_CW[base](cube)
        _BASE_CW[base](cube)
        _BASE_CW[base](cube)
    else:
        raise ValueError(f"Invalid move syntax: {move}")


def apply_move_sequence(cube: CubeState, moves: List[str]) -> None:
    """Apply a sequence of moves in-place."""
    for m in moves:
        apply_move(cube, m)


# Convenience mapping
MOVE_TABLE: Dict[str, Callable[[CubeState], None]] = {
    m: (lambda c, mm=m: apply_move(c, mm)) for m in MOVE_NAMES
}
