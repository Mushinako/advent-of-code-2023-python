# Day 12 (Hot Springs)

## Part 1

Part 1 is small enough to brute force by listing all possible spring configurations and
count them. It will take some time to run, maybe 30 seconds or so on a decent computer,
but it can be done (guess how I know this)

## Part 2

One common optimization for pattern matching is to use [dynamic programming][1], which
is a fancy word for caching intermediate data that will be reused. We can write a
recursive logic that processes the first damanged spring group size. See
`_get_possibilities_count` method in [the code][2] for implementation details

Similar to regex matching algorithms, this logic does a lot of back-tracking, and this
is where the caching shines, which essentially reduced the time complexity from about
exponential time to around polynomial time

[1]: https://en.wikipedia.org/wiki/Dynamic_programming#Computer_science
[2]: ./solution.py
