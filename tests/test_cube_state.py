from src.cube.cube_state import CubeState
from src.cube.move_generator import apply_move


def test_solved_cube():
    cube = CubeState.solved()
    assert cube.is_solved()


def test_copy_independence():
    cube = CubeState.solved()
    other = cube.copy()
    other.faces["U"][0] = "X"
    assert cube.faces["U"][0] != "X"
    assert not other.is_solved()


def test_move_changes_state():
    cube = CubeState.solved()
    apply_move(cube, "U")
    assert not cube.is_solved()
