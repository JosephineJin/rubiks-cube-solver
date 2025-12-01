"""
3D Rubik's Cube visualization using matplotlib.

We draw a solid cube with colored stickers on each face.
Coordinate convention (right-handed):
    x: left (-) to right (+)
    y: down (-) to up (+)
    z: back (-) to front (+)

Faces:
    U: y = +1
    D: y = -1
    F: z = +1
    B: z = -1
    R: x = +1
    L: x = -1
"""

from __future__ import annotations
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from ..cube.cube_state import CubeState, FACE_ORDER
from ..cube.move_generator import apply_move

# Map cube facelet letters to actual colors
COLOR_MAP: Dict[str, str] = {
    "U": "white",
    "D": "yellow",
    "F": "green",
    "B": "blue",
    "R": "red",
    "L": "orange",
}


def _sticker_vertices(face: str, row: int, col: int) -> List[Tuple[float, float, float]]:
    """
    Compute the 4 vertices of a single sticker square on a given face.

    row, col in {0,1,2}, where row=0 is "top", col=0 is "left"
    within that face's 3x3 grid.
    """
    # Each sticker is size 2/3, centered in [-1, 1] x [-1, 1]
    size = 2.0 / 3.0

    # In-face coordinates (u, v) in [-1, 1]
    # col: left (-1) -> right (+1)
    # row: top (+1)  -> bottom (-1)
    u0 = -1.0 + col * size
    u1 = u0 + size
    v0 = 1.0 - row * size
    v1 = v0 - size

    if face == "U":
        # y = +1, (x, z) plane
        return [
            (u0, 1.0, v0),
            (u1, 1.0, v0),
            (u1, 1.0, v1),
            (u0, 1.0, v1),
        ]
    elif face == "D":
        # y = -1
        return [
            (u0, -1.0, v1),
            (u1, -1.0, v1),
            (u1, -1.0, v0),
            (u0, -1.0, v0),
        ]
    elif face == "F":
        # z = +1, (x, y) plane
        return [
            (u0, v0, 1.0),
            (u1, v0, 1.0),
            (u1, v1, 1.0),
            (u0, v1, 1.0),
        ]
    elif face == "B":
        # z = -1
        # Flip x so it looks reasonable when rotated
        return [
            (-u1, v0, -1.0),
            (-u0, v0, -1.0),
            (-u0, v1, -1.0),
            (-u1, v1, -1.0),
        ]
    elif face == "R":
        # x = +1, (z, y) plane
        return [
            (1.0, v0, u0),
            (1.0, v0, u1),
            (1.0, v1, u1),
            (1.0, v1, u0),
        ]
    elif face == "L":
        # x = -1
        return [
            (-1.0, v0, -u1),
            (-1.0, v0, -u0),
            (-1.0, v1, -u0),
            (-1.0, v1, -u1),
        ]
    else:
        raise ValueError(f"Unknown face: {face}")


def _init_axes_3d(elev: float = 30.0, azim: float = 45.0):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_zlim([-1.5, 1.5])
    ax.view_init(elev=elev, azim=azim)
    ax.set_box_aspect([1, 1, 1])
    ax.axis("off")
    return fig, ax


def _create_cube_3d_patches(ax, state: CubeState) -> List[Poly3DCollection]:
    """
    Create all 54 sticker patches for the current state and return them
    as a flat list in a fixed order:

        for face in FACE_ORDER:
            for idx in 0..8:
                patches.append(poly_for(face, idx))

    We rely on this ordering in `update_cube_3d_patches`.
    """
    patches: List[Poly3DCollection] = []

    for face_name in FACE_ORDER:
        face = state.faces[face_name]
        for idx, color_code in enumerate(face):
            row, col = divmod(idx, 3)
            verts = _sticker_vertices(face_name, row, col)
            poly = Poly3DCollection([verts])
            poly.set_facecolor(COLOR_MAP.get(color_code, "gray"))
            poly.set_edgecolor("black")
            ax.add_collection3d(poly)
            patches.append(poly)

    return patches


def update_cube_3d_patches(patches: List[Poly3DCollection], state: CubeState) -> None:
    """
    Update the colors of the existing 3D patches to match the given state.
    Assumes patches are in the order produced by `_create_cube_3d_patches`.
    """
    idx = 0
    for face_name in FACE_ORDER:
        face = state.faces[face_name]
        for sticker_idx in range(9):
            color_code = face[sticker_idx]
            patches[idx].set_facecolor(COLOR_MAP.get(color_code, "gray"))
            idx += 1


def plot_cube_3d(state: CubeState, elev: float = 30.0, azim: float = 45.0) -> None:
    """
    Render a single CubeState as a 3D cube (static view).
    """
    fig, ax = _init_axes_3d(elev=elev, azim=azim)
    _create_cube_3d_patches(ax, state)
    plt.tight_layout()
    plt.show()


def init_live_cube_3d(state: CubeState, elev: float = 30.0, azim: float = 45.0):
    """
    Initialize a 3D figure + patches for live animation.

    Returns:
        fig, ax, patches
    """
    fig, ax = _init_axes_3d(elev=elev, azim=azim)
    patches = _create_cube_3d_patches(ax, state)
    fig.canvas.draw()
    plt.show(block=False)
    return fig, ax, patches


def animate_cube_3d(
    start: CubeState,
    moves: List[str],
    delay: float = 0.3,
    elev: float = 30.0,
    azim: float = 45.0,
    spin_per_move: float = 10.0,
) -> None:
    """
    Animate a sequence of moves in 3D starting from `start`.

    - Opens one 3D window.
    - Updates the cube colors in-place every move.
    - Slowly rotates the camera so the cube "spins" as it solves.
    """
    state = start.copy()
    fig, ax, patches = init_live_cube_3d(state, elev=elev, azim=azim)

    print("Initial state solved?", state.is_solved())

    total = len(moves)
    current_azim = azim

    for step, m in enumerate(moves, start=1):
        print(f"Move: {m}")
        apply_move(state, m)
        print("Solved?", state.is_solved())

        # Update colors
        update_cube_3d_patches(patches, state)

        # Spin the camera a little each move
        current_azim += spin_per_move
        ax.view_init(elev=elev, azim=current_azim)

        # Update title with progress + move name
        ax.set_title(f"3D View – Move {step}/{total}: {m}", fontsize=12)

        fig.canvas.draw()
        plt.pause(delay)

    print("Final solved?", state.is_solved())
    print("3D animation complete. Close the window to exit.")
    plt.show()
