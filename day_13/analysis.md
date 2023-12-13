# Day 13 (Point of Incidence)

## Part 1

This is another implementation problem, where we just follow the description and
implement the logic as-is: iterate through all the rows and columns, and see which
row/column can be used as a separation such that the reverse of the first part matches
the second part

## Part 2

At first I thought this is another optimization problem, but turns out it can be brute-
forced! Just flip all the cells one-by-one, and see which one returns a different
reflection. Do note that it's possible they also contain the same reflection, so we need
to skip the existing reflection in the logic
