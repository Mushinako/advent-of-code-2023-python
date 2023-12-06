# Day 06 (Wait For It)

## Part 1 & 2

**Note:** The numbers provided in the input are small enough to brute-force. Here's a
discussion for the non-brute-force solution

The distance travelled has a parabolic relationship to the amount of time by which the
acceleration button is held:

```text
d = t * (RT - t) = -t^2 + RT * t
```

The question is essentially asking for integer solutions to `d > DR`

```text
   -t^2 + RT * t > DR
=> t^2 - RT * t + DR < 0
=> (RT - sqrt(RT^2 - 4*DR)) / 2 < t < (RT + sqrt(RT^2 - 4*DR)) / 2
```

Calculate the values on both sides, and find the number of integers in between. Note
that both sides are exclusive less-thans, so if your calculations return integers, do
not include them in the final count

Note: glossary of variables used above:

| Variable | Meaning                                            |
| :------: | :------------------------------------------------- |
|   `t`    | Time variable                                      |
|   `d`    | Distance travelled                                 |
|   `wc`   | Number of different ways to win (win count)        |
|   `RT`   | Total race time (constant given per race)          |
|   `DR`   | Distance record for race (constant given per race) |
