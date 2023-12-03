# Day 03 (Gear Ratios)

## Part 1

The core logic is to iterate through all cells, find the symbols, and find the numbers
adjacent to each symbol. The tricky part is that numbers next to symbols can take up
multiple cells, and it's imperative to not miss or double-count any

For this, I first gather all 3 (corner) or 5 (side) 8 (center) neighbor coordinates for
a symbol cell into a set. To find an adjacent number, I start with a coordinate in the
set, see if it's a digit or not; if so, expand left and right until we hit a non-digit
cell or the edge. For each adjacent number I found, I remove all coordinates that this
number occupy from the set to avoid double-counting

## Part 2

I'm lucky enough to have part 1 work out most of the logic so that I can just repurpose
it. Instead of checking all non-digit non-dot symbols, only check stars; instead of
summing the adjacent numbers, check if there are only 2 adjacent numbers and multiply
them
