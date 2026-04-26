#!/usr/bin/env python3
"""
Conway's Game of Life — Python
Jayesh Puri

Run:  python3 life.py [rows] [cols] [generations]

Toroidal grid (edges wrap). Seeds with a Gosper Glider Gun
if the grid is big enough, otherwise random.
"""

import sys, os, time, random

ROWS = int(sys.argv[1]) if len(sys.argv) > 1 else 24
COLS = int(sys.argv[2]) if len(sys.argv) > 2 else 60
GENS = int(sys.argv[3]) if len(sys.argv) > 3 else 80

def empty_grid():
    return [[0]*COLS for _ in range(ROWS)]

def seed_random(grid, density=0.2):
    for row in range(ROWS):
        for col in range(COLS):
            grid[row][col] = 1 if random.random() < density else 0

def place_pattern(grid, pattern, start_row=0, start_col=0):
    """put a list of (delta_row, delta_col) offsets onto the grid"""
    for delta_row, delta_col in pattern:
        grid[(start_row + delta_row) % ROWS][(start_col + delta_col) % COLS] = 1

# the classic gosper glider gun — 36 cells that produce
# an infinite stream of gliders (period 30)
GLIDER_GUN = [
    (0,24),(1,22),(1,24),
    (2,12),(2,13),(2,20),(2,21),(2,34),(2,35),
    (3,11),(3,15),(3,20),(3,21),(3,34),(3,35),
    (4,0),(4,1),(4,10),(4,16),(4,20),(4,21),
    (5,0),(5,1),(5,10),(5,14),(5,16),(5,17),(5,22),(5,24),
    (6,10),(6,16),(6,24),
    (7,11),(7,15),
    (8,12),(8,13),
]

GLIDER = [(0,1),(1,2),(2,0),(2,1),(2,2)]

def draw(grid, generation):
    sys.stdout.write("\033[H")
    print(f"Game of Life  |  gen {generation}  |  {ROWS}x{COLS}")
    print()
    for row in grid:
        # alive = block char, dead = space
        print("".join("█" if cell else " " for cell in row))

def count_neighbors(grid, row, col):
    """count the 8 surrounding cells (wrapping at edges)"""
    total = 0
    for delta_row in (-1, 0, 1):
        for delta_col in (-1, 0, 1):
            if delta_row == 0 and delta_col == 0:
                continue
            total += grid[(row + delta_row) % ROWS][(col + delta_col) % COLS]
    return total

# -------------------------------------------------------
# Next generation — ITERATION
#
# Go through every cell, count neighbors, apply rules:
#   alive + 2 or 3 neighbors  ->  stay alive
#   alive + otherwise         ->  die
#   dead  + exactly 3         ->  come alive
#   dead  + otherwise         ->  stay dead
#
# We write into a fresh grid so reads don't see writes.
# -------------------------------------------------------
def step(grid):
    new_grid = empty_grid()
    for row in range(ROWS):
        for col in range(COLS):
            neighbors = count_neighbors(grid, row, col)
            if grid[row][col]:
                new_grid[row][col] = 1 if neighbors in (2, 3) else 0
            else:
                new_grid[row][col] = 1 if neighbors == 3 else 0
    return new_grid


if __name__ == "__main__":
    grid = empty_grid()

    # use glider gun on big grids, random on small ones
    if ROWS >= 12 and COLS >= 40:
        place_pattern(grid, GLIDER_GUN, 2, 2)
        place_pattern(grid, GLIDER, 15, 15)
    else:
        seed_random(grid)

    os.system("clear")

    for generation in range(GENS):    # main loop — ITERATION over generations
        draw(grid, generation)
        time.sleep(0.1)
        grid = step(grid)

    draw(grid, GENS)
    print(f"\nFinished {GENS} generations.")
