# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    from typing import Self


@dataclass(frozen=True, kw_only=True)
class _Card:
    index: int
    winning_nums: tuple[int, ...]
    containing_nums: tuple[int, ...]
    won_nums_count: int = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "won_nums_count",
            len(set(self.containing_nums) & set(self.winning_nums)),
        )

    @classmethod
    def from_str(cls, s: str) -> Self:
        index_str, nums_str = s.lower().removeprefix("card").split(":")
        index = int(index_str.strip())
        winning_nums_str, containing_nums_str = nums_str.strip().split("|")
        winning_nums = tuple(map(int, winning_nums_str.strip().split()))
        containing_nums = tuple(map(int, containing_nums_str.strip().split()))
        return cls(
            index=index, winning_nums=winning_nums, containing_nums=containing_nums
        )


class Solution(SolutionAbstract):
    day = 4
    data: list[_Card]

    def _process_data(self, raw_data: list[str]) -> list[_Card]:
        """
        Process day 04 data.
        """
        return [_Card.from_str(row) for row in raw_data]

    def part_1(self) -> int:
        """
        Day 04 part 1 solution.
        """
        points = 0
        for card in self.data:
            if card.won_nums_count > 0:
                points += 1 << (card.won_nums_count - 1)
        return points

    def part_2(self) -> int:
        """
        Day 04 part 2 solution.
        """
        count_map = [1] * len(self.data)
        for card in self.data:
            for i in range(card.index, card.index + card.won_nums_count):
                count_map[i] += count_map[card.index - 1]
        return sum(count_map)
