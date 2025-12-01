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
        ax.set_title("2D View – Start", fontsize=12)
        fig.canvas.draw()
        plt.show(block=False)

    total = len(moves)

    for step, m in enumerate(moves, start=1):
        print(f"Move: {m}")
        apply_move(state, m)
        print("Solved?", state.is_solved())

        if use_plot and patch_map is not None:
            update_cube_patches(patch_map, state)
            # Update title with progress + move name
            ax = plt.gca()
            ax.set_title(f"2D View – Move {step}/{total}: {m}", fontsize=12)
            fig.canvas.draw()
            plt.pause(delay)
        else:
            time.sleep(delay)

    print("Final solved?", state.is_solved())

    if use_plot:
        ax = plt.gca()
        ax.set_title("2D View – Final", fontsize=12)
        plt.pause(0.001)
        print("2D animation complete. Close the figure window to exit.")
        plt.show()
