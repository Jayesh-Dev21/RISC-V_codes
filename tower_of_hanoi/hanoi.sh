#!/usr/bin/env bash
#
# Tower of Hanoi in Bash
# - Jayesh Puri
#
# Usage: ./hanoi.sh [num_disks]
# Demonstrates recursion with a simple ASCII visualisation.
#

num_disks=${1:-4}
moves=0

declare -a PEG_A=()  # source peg
declare -a PEG_B=()  # auxiliary peg
declare -a PEG_C=()  # destination peg

# fill peg A with disks n..1 (ITERATION)
for (( i=num_disks; i>=1; i-- )); do
    PEG_A+=("$i")
done

# ---- draw the current state of all 3 pegs ----
draw() {
    echo ""
    # go through rows top-to-bottom (ITERATION over rows)
    for (( row=num_disks-1; row>=0; row-- )); do
        for peg in PEG_A PEG_B PEG_C; do
            local -n ref=$peg
            if (( row < ${#ref[@]} )); then
                local size=${ref[$row]}
                local gap=$(( num_disks - size ))
                printf "%*s" "$gap" ""
                for (( d=0; d<size; d++ )); do printf "="; done
                printf "|"
                for (( d=0; d<size; d++ )); do printf "="; done
                printf "%*s" "$gap" ""
            else
                printf "%*s|%*s" "$num_disks" "" "$num_disks" ""
            fi
            printf "  "
        done
        echo ""
    done
    # base
    for _ in 1 2 3; do
        for (( b=0; b<(2*num_disks+1); b++ )); do printf "-"; done
        printf "  "
    done
    echo ""
    printf "%*sA%*s  %*sB%*s  %*sC%*s\n" "$num_disks" "" "$num_disks" "" "$num_disks" "" "$num_disks" "" "$num_disks" "" "$num_disks" ""
    echo ""
}

# move top disk between two pegs
do_move() {
    local source=$1 dest=$2
    local -n source_peg=$source
    local -n dest_peg=$dest

    local disk=${source_peg[-1]}
    unset 'source_peg[-1]'
    dest_peg+=("$disk")

    (( moves++ ))
    echo "Move $moves: disk $disk  ${source#PEG_} -> ${dest#PEG_}"
    draw
}

# =============================================
# Recursive solver  (this is the RECURSION part)
#
# The idea: to move n disks from source->dest,
# first get n-1 out of the way onto aux,
# then move the big one, then put n-1 back.
# =============================================
hanoi() {
    local count=$1 source=$2 aux=$3 dest=$4

    # base case - just one disk, move it directly
    if (( count == 1 )); then
        do_move "$source" "$dest"
        return
    fi

    # recurse: move n-1 disks to aux peg
    hanoi $((count - 1)) "$source" "$dest" "$aux"
    # move the bottom (biggest) disk
    do_move "$source" "$dest"
    # recurse: move n-1 from aux to dest
    hanoi $((count - 1)) "$aux" "$source" "$dest"
}

echo "== Tower of Hanoi (n=$num_disks) =="
echo "Start:"
draw

hanoi "$num_disks" PEG_A PEG_B PEG_C

echo "Done! $moves moves (minimum possible = $((2**num_disks - 1)))"
