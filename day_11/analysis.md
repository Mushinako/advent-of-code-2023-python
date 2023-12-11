# Day 11 (Cosmic Expansion)

## Part 1 & 2

Because the expansions applies to whole rows and whole columns, the order of the steps
for the shortest path does not matter (i.e., up-left should be the same distance as
left-up everywhere on the board). For simplicity sake, let's consider horizontal
movements first, and then vertical movements

If there is no expansion, the number of horizontal movements is simple: it's just the
difference between the column indices `col_high - col_low`. To add in the expansion, we
just need to figure out how many columns are expanding. We can gather how many columns
are within are occupied and subtract that from the number of columns between the two. Be
careful of off-by-one errors: the number of columns between the columns is
`col_high - col_low - 1`

Do the same to the vertical movements, and the values up, and that's the result for one
pair of galaxies. Do that for every other pair and sum them up, you'll then have the
final result
