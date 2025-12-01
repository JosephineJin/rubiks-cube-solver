"""
Move pruning helpers.

- Forbid immediate inverses (e.g. R followed by R').
- Forbid repeating the same face more than once in a row (e.g. R then R2).
"""

from __future__ import annotations


def _face(move: str) -> str:
    return move[0]


def _inverse(move: str) -> str:
    if len(move) == 1:
        return move + "'"
    if move[1] == "'":
        return move[0]
    if move[1] == "2":
        return move  # self-inverse
    raise ValueError(f"Invalid move: {move}")


def is_redundant(prev: str, curr: str) -> bool:
    """Return True if curr immediately undoes or duplicates prev."""
    if curr == _inverse(prev):
        return True
    if _face(prev) == _face(curr):
        # Avoid sequences like R then R2 or R then R'
        return True
    return False
