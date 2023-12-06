# Day 06 (Wait For It)

## Part 1 & 2

The distance travelled has a parabolic relationship to the amount of time by which the
acceleration button is held:

```text
d(t) = t * (race_time - t) = -t^2 + race_time * t
```

This is a parabola that opens downwards, which means that the middle continous part of
the button hold-time will be the answer

Parabolae are also symmetrical, which means the number of small hold-times that don't
break the record is the same as the number of big hold-times that don't break the record

Therefore, the solution is to find the smallest hold time `t_min` that breaks the
record, and the number of wins for the game would be:

```text
win_count = race_time + 1 - (t_min + 1) * 2 = race_time - t * 2 - 1
```

Both of the `+1`s are to count for the 0-second case
