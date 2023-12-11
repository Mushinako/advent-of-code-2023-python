# pyright: reportMissingTypeStubs=false

from __future__ import annotations

from utils import SolutionAbstract

from .data.part_1 import Hand as Part1Hand
from .data.part_2 import Hand as Part2Hand


class Solution(SolutionAbstract, day=7):
    def part_1(self, *, visualize: bool = False) -> int:
        """
        Day 07 part 1 solution.
        """
        ranked_hands = sorted(Part1Hand.from_row(row) for row in self.raw_data)
        return sum(rank * hand.bid for rank, hand in enumerate(ranked_hands, start=1))

    def part_2(self, *, visualize: bool = False) -> int:
        """
        Day 07 part 2 solution.
        """
        ranked_hands = sorted(Part2Hand.from_row(row) for row in self.raw_data)
        return sum(rank * hand.bid for rank, hand in enumerate(ranked_hands, start=1))
