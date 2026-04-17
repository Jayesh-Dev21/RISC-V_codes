#!/usr/bin/env python3
"""
Tower of Hanoi — Python
Jayesh Krishan Puri

Run:  python3 hanoi.py [num_disks]
"""

import sys, time

num_disks = int(sys.argv[1]) if len(sys.argv) > 1 else 4
moves = 0

# each peg is a list, index 0 = bottom
pegs = {
    "A": list(range(num_disks, 0, -1)),
    "B": [],
    "C": [],
}

def draw():
    """quick ascii render of the three pegs"""
    print()
    for row in range(num_disks - 1, -1, -1):   # top row first (ITERATION)
        for peg_name in "ABC":
            stack = pegs[peg_name]
            if row < len(stack):
                disk = stack[row]
                pad = num_disks - disk
                print(" "*pad + "="*disk + "|" + "="*disk + " "*pad, end="  ")
            else:
                print(" "*num_disks + "|" + " "*num_disks, end="  ")
        print()
    for _ in range(3):
        print("-"*(2*num_disks+1), end="  ")
    print()
    for label in "ABC":
        print(" "*num_disks + label + " "*num_disks, end="  ")
    print("\n")

def move_disk(source, dest):
    global moves
    disk = pegs[source].pop()
    pegs[dest].append(disk)
    moves += 1
    print(f"Move {moves}: disk {disk}  {source} -> {dest}")
    draw()
    time.sleep(0.12)

# -------------------------------------------------------
#  THE RECURSIVE PART
#
#  Classic divide-and-conquer:
#    1) move top n-1 disks out of the way (recursive)
#    2) move the big disk
#    3) move n-1 back on top (recursive)
#
#  Base case: n==1, just move it.
# -------------------------------------------------------
def hanoi(count, source, aux, dest):
    if count == 1:                          # base case
        move_disk(source, dest)
        return
    hanoi(count - 1, source, dest, aux)     # recurse
    move_disk(source, dest)
    hanoi(count - 1, aux, source, dest)     # recurse

if __name__ == "__main__":
    print(f"== Tower of Hanoi (n={num_disks}) ==")
    print("Start:")
    draw()
    hanoi(num_disks, "A", "B", "C")
    print(f"Done! {moves} moves (minimum possible = {2**num_disks - 1})")
