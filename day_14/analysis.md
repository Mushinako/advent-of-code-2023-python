# Day 14 (Parabolic Reflector Dish)

## Part 1

This implementation is essentially to move all the `O`'s up in a 2D array until they hit
the boundary or a `#`. Personally I prefer to tranpose the array, roll west, and then
transpose back

## Part 2

1 billion cycles is a lot of cycles, so many such that I'm pretty sure the same platform
configuration will occur within the 1 billion cycles. Because the cycles are
deterministic, i.e., the same platform configuration before a cycle always produces the
configuration after the cycle, there will be loops of configurations within the 1
billion cycles. If we figure out the loop size, then we can cut the number of iterations
down from 1 billion. In my case, the loop size is 59, and I only had to run 184 cycles
to find the answer

Note that my implementations for individual rolls are not the most optimized. Gladly I
don't have to optimize them
