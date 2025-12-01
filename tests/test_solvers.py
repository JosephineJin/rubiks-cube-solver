from src.cube.cube_state import CubeState
from src.cube.scrambler import apply_random_scramble
from src.solvers.iddfs_solver import IDDFSSolver
from src.solvers.ida_star_solver import IDAStarSolver
from src.heuristics.corner_perm_pdb import CornerPermPDB
from src.utils.validator import validate_solution


def test_iddfs_on_easy_scramble():
    cube = CubeState.solved()
    # Very short scramble so IDDFS can handle it.
    scramble = ["U", "R", "U'"]
    for m in scramble:
        from src.cube.move_generator import apply_move

        apply_move(cube, m)
    solver = IDDFSSolver(max_depth=6)
    solution = solver.solve(cube)
    assert validate_solution(cube, solution)


def test_ida_star_on_random_small_scramble():
    cube = CubeState.solved()
    apply_random_scramble(cube, length=4)
    heuristic = CornerPermPDB()
    solver = IDAStarSolver(heuristic=heuristic.h, max_depth=10)
    solution = solver.solve(cube)
    assert validate_solution(cube, solution)
