# Advent of Code 2023 (Python)

My solutions to [Advent of Code 2023](https://adventofcode.com/2023) in Python

**SPOILER ALERT:** This repository contains contest solutions. The solutions will be
uploaded at least 30 minutes after the start of each day's contest.

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
