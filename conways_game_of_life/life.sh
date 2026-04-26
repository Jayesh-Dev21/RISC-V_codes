#!/usr/bin/env bash
#
# Conway's Game of Life in Bash
# Jayesh Puri
#
# Usage: ./life.sh [rows] [cols] [generations]
#
# Uses a flat 1D array because bash doesn't have 2D arrays.
# Grid wraps around (toroidal) so we don't need edge-case logic.
#

ROWS=${1:-20}
COLS=${2:-40}
GENS=${3:-50}

declare -a grid=()
declare -a buffer=()

# seed with random cells (~20% density)
for (( i=0; i<ROWS*COLS; i++ )); do
    grid[$i]=$(( RANDOM % 5 == 0 ? 1 : 0 ))
done

draw() {
    printf "\033[H"  # cursor home
    echo "Game of Life  |  gen $1  |  ${ROWS}x${COLS}"
    echo ""
    for (( row=0; row<ROWS; row++ )); do
        local line=""
        for (( col=0; col<COLS; col++ )); do
            local index=$(( row*COLS + col ))
            if (( grid[index] )); then line+="█"; else line+=" "; fi
        done
        echo "$line"
    done
}

# count live neighbors (ITERATION over the 8 offsets)
count_neighbors() {
    local row=$1 col=$2 count=0
    for delta_r in -1 0 1; do
        for delta_c in -1 0 1; do
            (( delta_r == 0 && delta_c == 0 )) && continue
            local neighbor_r=$(( (row + delta_r + ROWS) % ROWS ))
            local neighbor_c=$(( (col + delta_c + COLS) % COLS ))
            (( count += grid[neighbor_r*COLS + neighbor_c] ))
        done
    done
    echo $count
}

# compute next generation
# This is the main ITERATION — we loop over every cell and
# apply the 4 rules:
#   <2 neighbors  -> die  (underpopulation)
#   2-3 neighbors -> live (survival)
#   >3 neighbors  -> die  (overcrowding)
#   dead + 3      -> live (reproduction)
step() {
    buffer=()
    for (( row=0; row<ROWS; row++ )); do
        for (( col=0; col<COLS; col++ )); do
            local index=$(( row*COLS + col ))
            local alive=${grid[$index]}
            local neighbors
            neighbors=$(count_neighbors "$row" "$col")

            if (( alive )); then
                (( neighbors == 2 || neighbors == 3 )) && buffer[$index]=1 || buffer[$index]=0
            else
                (( neighbors == 3 )) && buffer[$index]=1 || buffer[$index]=0
            fi
        done
    done
    grid=("${buffer[@]}")
}

# --- main loop (ITERATION over generations) ---
clear
for (( gen=0; gen<GENS; gen++ )); do
    draw "$gen"
    sleep 0.15
    step
done
draw "$GENS"
echo ""
echo "Finished $GENS generations."
