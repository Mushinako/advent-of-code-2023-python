# Day 05 (If You Give A Seed A Fertilizer)

## Part 1

The optimization here is to not store every possible mapping of each categories in a
hashmap, as that will take lots of memory and lots of time to construct.

Instead, just store the ranges as-is, and iterate through them to find if any of the
ranges contain the number you want to check. If found, then get the number from that
range; if the number is in none of the ranges, then return the number itself. A small
optimization is adding binary searches, offering `O(log n)` time complexity. Check
`_AlmanacMap.forward_get` for implementation

## Part 2

Now that the seeds are also in ranges with hundreds of millions of members each, we need
to think of a way to not check all seed numbers.

Because we only care about the lowest location number, and the destination number
increases with the source number _within the same range_, we only need to consider the
start of each range, as any other number within the same range will produce a large
destination number.

The tricky part is that because there are 7 levels of ranges, they can overlap with one
another. Consider a mapping like:

```text
seed-to-soil map:
3 1 10  -> seeds 1-10 maps to soils 3-12
1 11 2  -> seeds 11-12 maps to soils 1-2

soil-to-fertilizer map:
5 2 4   -> soils 2-5 maps to fertilizers 5-8
10 6 3  -> soils 6-8 maps to fertilizers 10-12
2 10 3  -> soils 10-12 maps to fertilizers 2-4
```

Overall, the mapping for seeds 1-12 looks like:

| Seed | Soil | Fertilizer |                  |
| :--: | :--: | :--------: | :--------------- |
|  1   |  3   |     6      | Seed range start |
|  2   |  4   |     7      |                  |
|  3   |  5   |     8      |                  |
|  4   |  6   |     10     | Soil range start |
|  5   |  7   |     11     |                  |
|  6   |  8   |     12     |                  |
|  7   |  9   |     9      |                  |
|  8   |  10  |     2      | Soil range start |
|  9   |  11  |     3      |                  |
|  10  |  12  |     4      |                  |
|  11  |  1   |     1      | Seed range start |
|  12  |  2   |     5      | Soil range start |

Seed numbers 1 and 11 and soil numbers 2, 6, and 10 and range starts. They hold the
potential of producing the lowest numbers in the next levels, so it's only necessary to
consider these.

For simplicity, we can convert all the non-seed starts (in this case, soil numbers 2, 6,
and 10) back to seed numbers (12, 4, and 8 respectively). This will require some form of
backwards number translation from destination numbers to source numbers. The logic is
roughly the same as the forward logic, just with some fields swapped, and the
implementation is in `_AlmanacMap.backward_get`. With this we can get all the seed
number candidates (in this case, 1, 4, 8, 11, 12)

With the candidates in hand, we can find the candidates within each range and check
which candidate produces the lowest final number. Do note that the start of each ranges
should be included as well. E.g., if we want to check `3 7`, which translates to seeds
3-9, we need to check seeds 3, 4, and 8
