"""
Build a small edge-orientation-ish pattern database.

Usage (from project root):

    python -m src.heuristics.build_edge_orient_pdb

This will:
  - BFS from the solved cube up to MAX_DEPTH moves.
  - For each visited state, compute the EdgeOrientPDB pattern key.
  - Store the minimum depth (in quarter-turn metric) for each pattern.
  - Save to data/pattern_dbs/edge_orient_pdb.pkl.

The resulting PDB is not complete for the full cube state space,
but it gives a meaningful, precomputed lower bound for many patterns.
"""

from __future__ import annotations
from collections import deque
import time
from typing import Dict, Tuple

from src.cube.cube_state import CubeState
from src.cube.move_generator import MOVE_NAMES, apply_move
from src.utils.move_pruning import is_redundant
from src.heuristics.edge_orient_pdb import EdgeOrientPDB


# You can increase this to 6 if you have a powerful machine / time.
MAX_DEPTH = 5


def build_edge_orient_pdb() -> EdgeOrientPDB:
    pdb = EdgeOrientPDB()
    table: Dict[int, int] = {}

    start_state = CubeState.solved()
    start_key = pdb.encode(start_state)
    table[start_key] = 0

    # BFS queue: (state, depth, last_move)
    queue = deque([(start_state, 0, None)])
    visited = {start_state.to_string()}

    num_expanded = 0
    t0 = time.time()

    while queue:
        state, depth, last_move = queue.popleft()
        num_expanded += 1

        if num_expanded % 10000 == 0:
            elapsed = time.time() - t0
            print(
                f"Expanded {num_expanded} states, "
                f"current depth={depth}, "
                f"unique patterns={len(table)}, "
                f"time={elapsed:.1f}s"
            )

        # Record pattern for this state
        key = pdb.encode(state)
        if key not in table:
            table[key] = depth

        if depth >= MAX_DEPTH:
            continue

        for move in MOVE_NAMES:
            if last_move is not None and is_redundant(last_move, move):
                continue

            new_state = state.copy()
            apply_move(new_state, move)
            s_str = new_state.to_string()
            if s_str in visited:
                continue
            visited.add(s_str)
            queue.append((new_state, depth + 1, move))

    elapsed = time.time() - t0
    print(
        f"\nFinished BFS up to depth {MAX_DEPTH}. "
        f"Expanded {num_expanded} states, "
        f"unique patterns={len(table)}, "
        f"elapsed={elapsed:.1f}s"
    )

    pdb.table = table
    pdb.save()
    print(f"PDB saved to: {pdb.db_path}")
    return pdb


if __name__ == "__main__":
    build_edge_orient_pdb()
