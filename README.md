# Advent of Code 2023 (Python)

My solutions to [Advent of Code 2023](https://adventofcode.com/2023) in Python

**SPOILER ALERT:** This repository contains contest solutions. The solutions will be
uploaded at least 30 minutes after the start of each day's contest.

## Stats

### By Day

| Day                                  | Level 1 Rank | Level 2 Rank | Note |
| :----------------------------------- | :----------: | :----------: | :--- |
| 01 (Trebuchet?!)                     |     886      |     409      |      |
| 02 (Cube Conundrum)                  |     2332     |     1578     |      |
| 03 (Gear Ratios)                     |     1074     |     458      |      |
| 04 (Scratchcards)                    |     2659     |     1298     |      |
| 05 (If You Give A Seed A Fertilizer) |     3170     |     3117     |      |
| 06 ()                                |              |              |      |
| 07 ()                                |              |              |      |
| 08 ()                                |              |              |      |
| 09 ()                                |              |              |      |
| 10 ()                                |              |              |      |
| 11 ()                                |              |              |      |
| 12 ()                                |              |              |      |
| 13 ()                                |              |              |      |
| 14 ()                                |              |              |      |
| 15 ()                                |              |              |      |
| 16 ()                                |              |              |      |
| 17 ()                                |              |              |      |
| 18 ()                                |              |              |      |
| 19 ()                                |              |              |      |
| 20 ()                                |              |              |      |
| 21 ()                                |              |              |      |
| 22 ()                                |              |              |      |
| 23 ()                                |              |              |      |
| 24 ()                                |              |              |      |
| 25 ()                                |              |              |      |

### By Leaderboard (as of 2023-12-05 01:46 EDT)

| Leaderboard | Score | Rank |
| :---------- | :---: | :--: |
| Worldwide   |   0   |      |
| PyDis       | 10753 |  22  |
| PyDis Staff |  794  |  4   |

## How to Use this Repo?

1. Create a `config.yml` in the root of this repository. Put your AoC token in. You can
   find the token when you inspect the request cookies on AoC's website when you're
   logged in. Put it in `config.yml` as:

   ```yaml
   cookies:
     session: "Your session key"
   ```

2. Create a virtual environment and install the dependencies in `pyproject.toml`
3. To download an input, run `python run.py d <day>`
4. To print calculated result for part 1/2, run `python run.py p <day> 1|2`
5. To submit calculated result for part 1/2, run `python run.py s <day> 1|2`
