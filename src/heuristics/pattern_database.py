"""
Pattern Database (PDB) base class.

This file provides the interface and simple on-disk caching helpers.
You can plug in more sophisticated PDB construction later.
"""

from __future__ import annotations
import os
import pickle
from abc import ABC, abstractmethod
from typing import Dict, Tuple
from ..cube.cube_state import CubeState


class PatternDatabase(ABC):
    """
    Base class for pattern databases.

    For now:
    - `table` maps compressed state -> distance
    - `h(state)` falls back to 0 if table is empty.
    """

    def __init__(self, db_path: str | None = None):
        self.table: Dict[Tuple, int] = {}
        self.db_path = db_path
        if db_path is not None and os.path.exists(db_path):
            self._load()

    @abstractmethod
    def encode(self, state: CubeState) -> Tuple:
        """Encode a cube state into a compact key."""
        raise NotImplementedError

    def h(self, state: CubeState) -> int:
        """Lookup heuristic value. Defaults to 0 if not found."""
        key = self.encode(state)
        return self.table.get(key, 0)

    def _load(self) -> None:
        with open(self.db_path, "rb") as f:
            self.table = pickle.load(f)

    def save(self) -> None:
        if self.db_path is None:
            raise ValueError("db_path is not set")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, "wb") as f:
            pickle.dump(self.table, f)
