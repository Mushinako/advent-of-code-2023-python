# Day 10 (Pipe Maze)

## Part 1

We can traverse through the loop and see how long the whole loop is. Half of that size
would give the distance to the farthest point via the loop

Note that the loop size has to be even. For the animal to go through the loop and back
to the starting point, it must go an even number of steps on the north-south direction
and an even number of steps on the east-west direction, so the loop size has to be even
as well

This implementation assumes that only 2 pipes stem from the animal's place, which the
data seems to conform to

## Part 2

If the loop doesn't touch itself, one usual way of checking whether a point is inside or
outside a loop is to check if there's a path from it to the edge of the field. In fact,
we can do a small change to this field to make that apply: scale the field up by 2x. For
example, for loop (`*` is used in place of `.` to denote ground cells for clarity)

```text
*┌────┐┌┐┌┐┌┐┌─┐****
*│┌──┐││││││││┌┘****
*││*┌┘││││││││└┐****
┌┘└┐└┐└┘└┘││└┘*└─┐**
└──┘*└┐***└┘┌┐┌─┐└┐*
****┌─┘**┌┐┌┘│└┐└┐└┐
****└┐*┌┐││└┐│*└┐└┐│
*****│┌┘└┘│┌┘│┌┐│*└┘
****┌┘└─┐*││*││││***
****└───┘*└┘*└┘└┘***
```

We multiple each cell's `row` and `col` indices (0-based) by 2 (note the new blanks in
between, denoted by `.`)

```text
*.┌.─.─.─.─.┐.┌.┐.┌.┐.┌.┐.┌.─.┐.*.*.*.*
.......................................
*.│.┌.─.─.┐.│.│.│.│.│.│.│.│.┌.┘.*.*.*.*
.......................................
*.│.│.*.┌.┘.│.│.│.│.│.│.│.│.└.┐.*.*.*.*
.......................................
┌.┘.└.┐.└.┐.└.┘.└.┘.│.│.└.┘.*.└.─.┐.*.*
.......................................
└.─.─.┘.*.└.┐.*.*.*.└.┘.┌.┐.┌.─.┐.└.┐.*
.......................................
*.*.*.*.┌.─.┘.*.*.┌.┐.┌.┘.│.└.┐.└.┐.└.┐
.......................................
*.*.*.*.└.┐.*.┌.┐.│.│.└.┐.│.*.└.┐.└.┐.│
.......................................
*.*.*.*.*.│.┌.┘.└.┘.│.┌.┘.│.┌.┐.│.*.└.┘
.......................................
*.*.*.*.┌.┘.└.─.┐.*.│.│.*.│.│.│.│.*.*.*
.......................................
*.*.*.*.└.─.─.─.┘.*.└.┘.*.└.┘.└.┘.*.*.*
```

Then, fill in the gaps within the loop

```text
*.┌─────────┐.┌─┐.┌─┐.┌─┐.┌───┐.*.*.*.*
..│.........│.│.│.│.│.│.│.│...│........
*.│.┌─────┐.│.│.│.│.│.│.│.│.┌─┘.*.*.*.*
..│.│.....│.│.│.│.│.│.│.│.│.│..........
*.│.│.*.┌─┘.│.│.│.│.│.│.│.│.└─┐.*.*.*.*
..│.│...│...│.│.│.│.│.│.│.│...│........
┌─┘.└─┐.└─┐.└─┘.└─┘.│.│.└─┘.*.└───┐.*.*
│.....│...│.........│.│...........│....
└─────┘.*.└─┐.*.*.*.└─┘.┌─┐.┌───┐.└─┐.*
............│...........│.│.│...│...│..
*.*.*.*.┌───┘.*.*.┌─┐.┌─┘.│.└─┐.└─┐.└─┐
........│.........│.│.│...│...│...│...│
*.*.*.*.└─┐.*.┌─┐.│.│.└─┐.│.*.└─┐.└─┐.│
..........│...│.│.│.│...│.│.....│...│.│
*.*.*.*.*.│.┌─┘.└─┘.│.┌─┘.│.┌─┐.│.*.└─┘
..........│.│.......│.│...│.│.│.│......
*.*.*.*.┌─┘.└───┐.*.│.│.*.│.│.│.│.*.*.*
........│.......│...│.│...│.│.│.│......
*.*.*.*.└───────┘.*.└─┘.*.└─┘.└─┘.*.*.*
```

For easy of calculation, we can pad a layer on the outside to denote the boundary of the
field. If a cell has a path to this boundary, then it's outside the loop. Below the
boundary is denoted `+`

```text
+++++++++++++++++++++++++++++++++++++++++
+*.┌─────────┐.┌─┐.┌─┐.┌─┐.┌───┐.*.*.*.*+
+..│.........│.│.│.│.│.│.│.│...│........+
+*.│.┌─────┐.│.│.│.│.│.│.│.│.┌─┘.*.*.*.*+
+..│.│.....│.│.│.│.│.│.│.│.│.│..........+
+*.│.│.*.┌─┘.│.│.│.│.│.│.│.│.└─┐.*.*.*.*+
+..│.│...│...│.│.│.│.│.│.│.│...│........+
+┌─┘.└─┐.└─┐.└─┘.└─┘.│.│.└─┘.*.└───┐.*.*+
+│.....│...│.........│.│...........│....+
+└─────┘.*.└─┐.*.*.*.└─┘.┌─┐.┌───┐.└─┐.*+
+............│...........│.│.│...│...│..+
+*.*.*.*.┌───┘.*.*.┌─┐.┌─┘.│.└─┐.└─┐.└─┐+
+........│.........│.│.│...│...│...│...│+
+*.*.*.*.└─┐.*.┌─┐.│.│.└─┐.│.*.└─┐.└─┐.│+
+..........│...│.│.│.│...│.│.....│...│.│+
+*.*.*.*.*.│.┌─┘.└─┘.│.┌─┘.│.┌─┐.│.*.└─┘+
+..........│.│.......│.│...│.│.│.│......+
+*.*.*.*.┌─┘.└───┐.*.│.│.*.│.│.│.│.*.*.*+
+........│.......│...│.│...│.│.│.│......+
+*.*.*.*.└───────┘.*.└─┘.*.└─┘.└─┘.*.*.*+
+++++++++++++++++++++++++++++++++++++++++
```

The overall transformation for all of the original cells is `(2*row+1, 2*col+1)`

Note that we only care about the original cells (denoted `*`). In the final count we
don't want to include the cells we added (`.` and `+`). We can identify them by odd
`row` and `col` values

Now is the time to identify which points are outside and which ones are inside. Start
from a point on the boundary (e.g., `(0, 0)`) and traverse the field to find all the
points it can reach. Those that it cannot reach are the points inside the loop. Count
the number of unreached points that have odd `row` and `col`, and you're done!
