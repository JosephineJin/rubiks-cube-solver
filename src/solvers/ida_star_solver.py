"""
Iterative Deepening A* (IDA*) solver.
"""

from __future__ import annotations
from typing import Callable, List, Optional
from .base_solver import BaseSolver
from ..cube.cube_state import CubeState
from ..cube.move_generator import MOVE_NAMES, apply_move
from ..utils.move_pruning import is_redundant


Heuristic = Callable[[CubeState], int]


class IDAStarSolver(BaseSolver):
    def __init__(self, heuristic: Heuristic, max_depth: int = 40):
        self.heuristic = heuristic
        self.max_depth = max_depth

    def solve(self, start: CubeState) -> List[str]:
        if start.is_solved():
            return []

        bound = self.heuristic(start)
        path: List[str] = []

        while bound <= self.max_depth:
            t = self._search(start.copy(), path, 0, bound, None)
            if isinstance(t, list):  # found solution
                return t
            if t == float("inf"):
                break
            bound = int(t)

        raise RuntimeError("IDA* failed to find solution within depth bound")

    def _search(
        self,
        node: CubeState,
        path: List[str],
        g: int,
        bound: int,
        last_move: Optional[str],
    ) -> int | List[str]:
        f = g + self.heuristic(node)
        if f > bound:
            return f
        if node.is_solved():
            return list(path)

        min_over = float("inf")

        for move in MOVE_NAMES:
            if last_move is not None and is_redundant(last_move, move):
                continue

            new_node = node.copy()
            apply_move(new_node, move)
            path.append(move)
            t = self._search(new_node, path, g + 1, bound, move)
            if isinstance(t, list):
                return t
            if t < min_over:
                min_over = t
            path.pop()

        return min_over
