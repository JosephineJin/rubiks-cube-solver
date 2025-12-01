# src/visualization/cube_viewer.py

"""
Simple matplotlib viewer for a cube state.

We draw a 2D net of the cube:

      U
    L F R B
      D
"""

from __future__ import annotations
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
from ..cube.cube_state import CubeState, FACE_ORDER

COLOR_MAP: Dict[str, str] = {
    "U": "white",
    "R": "red",
    "F": "green",
    "D": "yellow",
    "L": "orange",
    "B": "blue",
}


def _init_axes() -> Tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1, 13)
    ax.set_ylim(-4, 8)
    return fig, ax


def _draw_face_patches(ax, x0: int, y0: int) -> List[plt.Rectangle]:
    patches: List[plt.Rectangle] = []
    size = 1
    for i in range(3):
        for j in range(3):
            rect = plt.Rectangle(
                (x0 + j * size, y0 - i * size),
                size,
                size,
                edgecolor="black",
                facecolor="gray",
            )
            ax.add_patch(rect)
            patches.append(rect)
    return patches


def create_cube_patches(ax) -> Dict[Tuple[str, int], plt.Rectangle]:
    """
    Create all 54 patches (6 faces * 9 stickers) and return a mapping:
        (face_name, index) -> patch
    """
    patch_map: Dict[Tuple[str, int], plt.Rectangle] = {}

    coords = {
        "U": (3, 6),
        "L": (0, 3),
        "F": (3, 3),
        "R": (6, 3),
        "B": (9, 3),
        "D": (3, 0),
    }

    for face_name, (x0, y0) in coords.items():
        patches = _draw_face_patches(ax, x0, y0)
        for idx, p in enumerate(patches):
            patch_map[(face_name, idx)] = p

    return patch_map


def update_cube_patches(patch_map, state: CubeState) -> None:
    """
    Update existing patches to match the cube state.
    """
    for face_name in FACE_ORDER:
        face = state.faces[face_name]
        for idx in range(9):
            color_letter = face[idx]
            color = COLOR_MAP.get(color_letter, "gray")
            patch = patch_map[(face_name, idx)]
            patch.set_facecolor(color)


def plot_cube(state: CubeState) -> None:
    """
    Static plot of a single state.
    """
    fig, ax = _init_axes()
    patch_map = create_cube_patches(ax)
    update_cube_patches(patch_map, state)
    plt.show()
