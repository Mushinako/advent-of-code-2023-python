# Day 08 (Haunted Wasteland)

## Part 1

This part is brute-forced: construct the map, and follow the instructions

## Part 2

One intuition is that if you follow the instruction indefinitely, the path may go into
some kind of loop. With this thought, we can try to figure out how many steps it takes
to reach the first node that ends with `Z` and how many steps there are in the loop

Here are the data for my input:

```text
* min_step_count=14893, loop_size=14893
* min_step_count=20513, loop_size=20513
* min_step_count=22199, loop_size=22199
* min_step_count=19951, loop_size=19951
* min_step_count=17141, loop_size=17141
* min_step_count=12083, loop_size=12083
```

Curious to note that the two numbers are always the same. I highly suspect that this
input is intentionally constructed to make this calculation simple, because we can just
find the [least common multiple][1] and that would be the answer

Even if the two numbers are different, we can still solve it, albeit more complicatedly,
with [Chinese remaind theorem][2]. As it doesn't apply here I won't be discussing this.
If interested, you can check out the Wikipedia page linked or my write-up for
[AOC 2020 day 13 part 2][3]

Sidenote: Per [discussion within PyDis][4], it does feel like the data is specifically
constructed so that the number of steps to reach the first node that ends with `Z` is
the same as the number of steps in the loop

[1]: https://en.wikipedia.org/wiki/Least_common_multiple
[2]: https://en.wikipedia.org/wiki/Chinese_remainder_theorem
[3]: https://github.com/Mushinako/Advent-of-Code-2020/blob/main/Day_13/analysis.md#part-2
[4]: https://discord.com/channels/267624335836053506/897932085766004786/1182563238345453661
