# [Day 01 (Trebuchet?!)](https://adventofcode.com/2023/day/1)

## Part 1

This is a straightforward implementation: scan string left-to-right for the
digit, and then right-to-left for the second digit. Concatenate to get the
number to sum

## Part 2

This is roughly the same as part one, just with additional words to check.
Luckily Python has `str.startswith()` and `str.endswith()` for these checks.
Even if you're using a language that does not have this, you can still slice
the strings and do a direct comparison
