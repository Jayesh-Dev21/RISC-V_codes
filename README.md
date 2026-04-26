# RISC-V Coding Challenge

Jayesh Puri  
[github.com/Jayesh-Dev21](https://github.com/Jayesh-Dev21)

---

Both problems solved in **Bash** and **Python**.  
Recursion and iteration sections are commented inline in the source.

```
risc-v_task/
├── tower_of_hanoi/
│   ├── hanoi.sh
│   └── hanoi.py
├── conways_game_of_life/
│   ├── life.sh
│   └── life.py
├── coding_challenge.typ   <- typst PDF for submission
├── solution.txt           <- detailed walkthrough
└── README.md
```

---

## Running

**Hanoi** (default 4 disks):
```bash
bash tower_of_hanoi/hanoi.sh 4
python3 tower_of_hanoi/hanoi.py 4
```

**Game of Life** (rows, cols, generations):
```bash
bash conways_game_of_life/life.sh 20 40 50
python3 conways_game_of_life/life.py 24 60 80
```

---

## Problem 1 - Tower of Hanoi

Classic recursion problem. Move n disks from peg A to C, one at a time, never placing a bigger disk on a smaller one.

The trick is that moving n disks breaks down into:
1. Move top n-1 disks to the spare peg (same problem, smaller)
2. Move the big one
3. Move n-1 back on top

Base case is n=1 - just move it directly.

### Pseudocode

```
HANOI(n, source, aux, dest):
    if n == 1:
        move disk from source to dest     <- base case
        return

    HANOI(n-1, source, dest, aux)          <- recursion
    move disk from source to dest
    HANOI(n-1, aux, source, dest)          <- recursion
```

This gives exactly 2^n - 1 moves every time (optimal).

### Where recursion/iteration show up

- `hanoi()` is the recursive part — it calls itself twice for subproblems
- The init loop filling the starting peg and the `draw()` function both use iteration (for-loops over rows/pegs)

---

## Problem 2 - Conway's Game of Life

A cellular automaton where each cell is alive or dead, and the next state of the whole grid is computed from the current one using four rules:

1. Live cell with <2 neighbors dies (lonely)
2. Live cell with 2 or 3 neighbors lives
3. Live cell with >3 neighbors dies (overcrowded)
4. Dead cell with exactly 3 neighbors comes alive

The grid wraps around (toroidal) so there's no special edge handling.

### Pseudocode

```
STEP(grid):
    new = empty grid

    for each cell (r, c):                   <- iteration over grid
        n = count alive neighbors of (r, c) <- iteration over 8 offsets
        if cell is alive:
            new[r][c] = alive if n is 2 or 3
        else:
            new[r][c] = alive if n is exactly 3

    return new

main:
    grid = seed(pattern)
    for gen in 0..max:                      <- iteration over generations
        draw(grid)
        grid = STEP(grid)
```

### Where iteration shows up

Basically everywhere — nested loops over every cell, a loop over the 8 neighbor offsets, and the outer generation loop. There's no recursion in this problem at all.

---

## Quick Comparison

| | Hanoi | Game of Life |
|---|---|---|
| Main technique | Recursion | Iteration |
| Stops when | Base case (n=1) | Generation limit |
| Complexity | O(2^n) | O(rows × cols) per gen |
