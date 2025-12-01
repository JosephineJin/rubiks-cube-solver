from src.cube.cube_state import CubeState
from src.cube.move_generator import apply_move
from src.utils.validator import is_valid_move_sequence


def test_move_and_inverse():
    cube = CubeState.solved()
    apply_move(cube, "R")
    apply_move(cube, "R'")
    assert cube.is_solved()


def test_double_move_self_inverse():
    cube = CubeState.solved()
    apply_move(cube, "U2")
    apply_move(cube, "U2")
    assert cube.is_solved()


def test_move_sequence_validation():
    assert is_valid_move_sequence(["U", "R2", "F'", "L"])
    assert not is_valid_move_sequence(["X", "U2"])
