# Day 04 (Scratchcards)

## Part 1

The easiest way to check which numbers on the ticket are winning numbers is to do a set
intersection between the 2 number collections. The score of the card then can be
calculated by looking at the size of the intersection set

## Part 2

The basics of part 2 is to only keep track of the counts of each card instead of the
card themselves. Because the cards can only offer cards after them, we can go from the
first card to the last and not have to worry about counts of previous cards changing
