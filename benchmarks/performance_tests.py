"""
Simple performance test harness.

Usage:
    python -m benchmarks.performance_tests
"""

from __future__ import annotations
import time
from typing import List
from src.cube.cube_state import CubeState
from src.cube.scrambler import apply_random_scramble
from src.solvers.ida_star_solver import IDAStarSolver
from src.heuristics.corner_perm_pdb import CornerPermPDB
from src.utils.validator import validate_solution


def run_benchmark(num_scrambles: int = 5, scramble_length: int = 8) -> None:
    heuristic = CornerPermPDB()
    solver = IDAStarSolver(heuristic=heuristic.h, max_depth=30)

    times: List[float] = []
    lengths: List[int] = []

    for i in range(num_scrambles):
        cube = CubeState.solved()
        apply_random_scramble(cube, length=scramble_length)

        start = time.time()
        solution = solver.solve(cube)
        elapsed = time.time() - start

        assert validate_solution(cube, solution)
        times.append(elapsed)
        lengths.append(len(solution))
        print(f"Scramble {i+1}: time={elapsed:.3f}s, moves={len(solution)}")

    avg_t = sum(times) / len(times)
    avg_len = sum(lengths) / len(lengths)
    print(f"Average time: {avg_t:.3f}s, average solution length: {avg_len:.2f}")


if __name__ == "__main__":
    run_benchmark()
