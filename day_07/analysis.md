# Day 07 (Camel Cards)

## Part 1

It's another implementation day! Personally I find it easiest to make each card and each
hand objects and give custom implementations for comparisons so that they can be sorted.
The card-sorting is easy: just assign a number to each card; the hand sorting is
slightly trickier, as we need to figure out the type of the hand first, and then, order
by that, and then order by card values

## Part 2

The card value comparison logic is still the same, just reassign `J`'s value to a lower
one. The main change is in the logic that figures out hand types, as Jokers now act as
wildcards. The easier way is to count Jokers separately, and add their count to the
cards with the most count when calculating hand type
