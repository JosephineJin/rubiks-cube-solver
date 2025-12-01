# src/visualization/animator.py

"""
Visualizer / animator utilities.

This version uses a single matplotlib window and updates it for each move.
"""

from __future__ import annotations
from typing import List
import time

import matplotlib.pyplot as plt

from ..cube.cube_state import CubeState
from ..cube.move_generator import apply_move
from .cube_viewer import _init_axes, create_cube_patches, update_cube_patches


def animate_solution(
    start: CubeState,
    moves: List[str],
    delay: float = 0.3,
    use_plot: bool = False,
) -> None:
    """
    Animate a sequence of moves starting from `start`.

    If use_plot is True:
      - One matplotlib figure is created.
      - The cube is redrawn in that same figure every move.
    """
    state = start.copy()
    print("Initial state solved?", state.is_solved())

    fig = None
    patch_map = None

    if use_plot:
        fig, ax = _init_axes()
        patch_map = create_cube_patches(ax)
        update_cube_patches(patch_map, state)
        fig.canvas.draw()
        plt.show(block=False)

    for m in moves:
        print(f"Move: {m}")
        apply_move(state, m)
        print("Solved?", state.is_solved())

        if use_plot and patch_map is not None:
            update_cube_patches(patch_map, state)
            fig.canvas.draw()
            plt.pause(delay)
        else:
            time.sleep(delay)

    print("Final solved?", state.is_solved())

    if use_plot:
        # Keep window open at the end until user closes it
        plt.pause(0.001)
        print("Animation complete. Close the figure window to exit.")
        plt.show()
