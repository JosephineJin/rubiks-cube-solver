# 3×3×3 Rubik's Cube Solver (CS 4260 AI Final Project)

This repository implements a heuristic-search based solver for the 3×3×3 Rubik's Cube.

## Features

- **Representation**: Facelet-based cube state with 6 faces (U, R, F, D, L, B).
- **Moves**: 18 quarter-turn metric moves (`U, U2, U', ..., B, B2, B'`).
- **Scrambler**: Random scramble generator.
- **Solvers**:
  - IDDFS (baseline)
  - IDA* (primary) with pluggable heuristics
- **Heuristics**:
  - Pattern database base class
  - Corner orientation / edge orientation / corner permutation heuristic shells
- **Visualization**:
  - Simple matplotlib-based cube viewer
  - Text-based solution animation
- **Benchmarks**: Basic performance test harness.
- **Tests**: Pytest-based unit tests for core components.

## Quickstart

```bash
pip install -r requirements.txt

# Run demo
python -m demos.demo

# Run tests
pytest
