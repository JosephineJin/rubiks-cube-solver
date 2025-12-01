"""
Baseline Iterative Deepening Depth-First Search solver.
"""

from __future__ import annotations
from typing import List, Optional
from .base_solver import BaseSolver
from ..cube.cube_state import CubeState
from ..cube.move_generator import MOVE_NAMES, apply_move
from ..utils.move_pruning import is_redundant


class IDDFSSolver(BaseSolver):
    def __init__(self, max_depth: int = 20):
        self.max_depth = max_depth

    def solve(self, start: CubeState) -> List[str]:
        if start.is_solved():
            return []

        for depth_limit in range(1, self.max_depth + 1):
            result = self._dfs(start, depth_limit)
            if result is not None:
                return result
        raise RuntimeError("No solution found within depth limit")

    def _dfs(
        self,
        start: CubeState,
        depth_limit: int,
    ) -> Optional[List[str]]:
        stack: List[tuple[CubeState, List[str]]] = [(start.copy(), [])]

        while stack:
            state, path = stack.pop()
            if state.is_solved():
                return path
            if len(path) >= depth_limit:
                continue

            prev = path[-1] if path else None
            for move in MOVE_NAMES:
                if prev is not None and is_redundant(prev, move):
                    continue

                new_state = state.copy()
                apply_move(new_state, move)
                stack.append((new_state, path + [move]))

        return None
