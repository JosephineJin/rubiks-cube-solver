from src.cube.cube_state import CubeState
from src.cube.move_generator import apply_move
from src.heuristics.corner_orient_pdb import CornerOrientPDB
from src.heuristics.edge_orient_pdb import EdgeOrientPDB
from src.heuristics.corner_perm_pdb import CornerPermPDB


def test_heuristics_zero_on_solved():
    cube = CubeState.solved()
    co = CornerOrientPDB()
    eo = EdgeOrientPDB()
    cp = CornerPermPDB()
    assert co.h(cube) == 0
    assert eo.h(cube) == 0
    assert cp.h(cube) == 0


def test_heuristics_nonzero_on_scrambled():
    cube = CubeState.solved()
    apply_move(cube, "U")
    cp = CornerPermPDB()
    assert cp.h(cube) >= 0
