"""
Main demo script for presentation.

Usage (from project root):

    python -m demos.demo               # default IDA*, length 6, no plot
    python -m demos.demo --plot        # show cube before/after
    python -m demos.demo --solver iddfs --length 4
"""

from __future__ import annotations
import argparse
import time

from src.cube.cube_state import CubeState
from src.cube.scrambler import apply_random_scramble
from src.solvers.iddfs_solver import IDDFSSolver
from src.solvers.ida_star_solver import IDAStarSolver
from src.heuristics.corner_perm_pdb import CornerPermPDB
from src.heuristics.edge_orient_pdb import EdgeOrientPDB
from src.utils.validator import validate_solution
from src.visualization.cube_viewer import plot_cube
from src.visualization.animator import animate_solution


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rubik's Cube solver demo")
    parser.add_argument(
        "--solver",
        choices=["ida", "iddfs"],
        default="ida",
        help="Which solver to use (default: ida)",
    )
    parser.add_argument(
        "--length",
        type=int,
        default=6,
        help="Scramble length (default: 6; use 4–6 for live demos).",
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Show matplotlib cube plots before/after solving.",
    )
    parser.add_argument(
        "--animate",
        action="store_true",
        help="Animate scramble + solution (with live cube visualization).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible scrambles (default: 42).",
    )
    return parser.parse_args()


def build_solver(name: str):
    if name == "iddfs":
        print("[Solver] Using IDDFS (uninformed search, small depth limit).")
        return IDDFSSolver(max_depth=12)

    elif name == "ida":
        # Use a combined heuristic:
        # - EdgeOrientPDB: PDB-based lower bound if table is built.
        # - CornerPermPDB: Hamming-like lower bound on corner permutations.
        edge_pdb = EdgeOrientPDB()
        corner_pdb = CornerPermPDB()

        def combined_h(state):
            return max(edge_pdb.h(state), corner_pdb.h(state))

        print(
            "[Solver] Using IDA* with combined heuristic:\n"
            f"          - EdgeOrientPDB (entries: {len(edge_pdb.table)})\n"
            "          - CornerPermPDB\n"
            "          Heuristic = max(edge_h, corner_h)"
        )
        return IDAStarSolver(heuristic=combined_h, max_depth=30)

    else:
        raise ValueError(f"Unknown solver: {name}")


def main() -> None:
    args = parse_args()

    # Fixed seed for deterministic scramble
    import random
    random.seed(args.seed)

    # Start from solved cube
    start = CubeState.solved()

    # Scramble
    scramble = apply_random_scramble(start, length=args.length)
    print("=" * 60)
    print(f"Scramble ({len(scramble)} moves):", " ".join(scramble))
    print("Scrambled solved?", start.is_solved())
    print("=" * 60)

    if args.plot:
        print("Showing scrambled cube...")
        plot_cube(start)

    # Build solver
    solver = build_solver(args.solver)
    print(f"\nUsing solver: {args.solver.upper()}")

    # Solve
    t0 = time.time()
    solution = solver.solve(start)
    elapsed = time.time() - t0

    print("\nSolution found!")
    print("Solution length:", len(solution))
    print("Solution moves:", " ".join(solution))
    print(f"Solve time: {elapsed:.3f} seconds")
    print("Solution valid?", validate_solution(start, solution))

    if args.plot:
        print("Showing cube after applying solution...")
        solved_copy = start.copy()
        from src.cube.move_generator import apply_move_sequence
        apply_move_sequence(solved_copy, solution)
        plot_cube(solved_copy)

    if args.animate:
        print("\nAnimating scramble + solution from solved state...")
        # Animate from solved: apply scramble then solution
        animate_solution(
            CubeState.solved(),
            scramble + solution,
            delay=0.2,
            use_plot=True,
        )


if __name__ == "__main__":
    main()
