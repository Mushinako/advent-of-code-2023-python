# Day 09 (Mirage Maintenance)

## Part 1

The crucial discovery here is that the next value is the sum of all last values of all
levels, as each value is the sum of the value to the left and that to the bottom-left:

```text
...         177*  201 (=177+16+6+2)
...      16*   24 (=16+6+2)
...    6*    8 (=6+2)
... 2*    2 (=2)
...    0 (ignored because it's always 0)
```

Therefore, we just need to calculate all the levels, and add up the last values of each
level to get our result

## Part 2

This is very similar to part 1, but instead of adding, we're doing subtraction this time

```text
(=0-7+3-1) -5     0* ...
     (=7-3+1) 5     7* ...
          (=3-1) 2     3* ...
               (=1) 1     1* ...
                       0 (ignored because it's always 0)
```

The pattern is that from the top, the odd levels are added, and the even levels are
subtracted
