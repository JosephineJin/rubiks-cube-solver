"""
Abstract solver interface.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from ..cube.cube_state import CubeState


class BaseSolver(ABC):
    """Abstract base class for Rubik's Cube solvers."""

    @abstractmethod
    def solve(self, start: CubeState) -> List[str]:
        """Return a sequence of moves that solves the cube."""
        raise NotImplementedError
