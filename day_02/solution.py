# pyright: reportMissingTypeStubs=false

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    from typing import Self


@dataclass(frozen=True, kw_only=True)
class _Game:
    id: int
    reveals: list[_CubeReveal]

    @classmethod
    def from_str(cls, s: str) -> Self:
        id_str, reveals_str = s.lower().removeprefix("game").split(":")
        id_ = int(id_str.strip())
        reveals = [
            _CubeReveal.from_str(s.strip()) for s in reveals_str.strip().split(";")
        ]
        return cls(id=id_, reveals=reveals)


@dataclass(frozen=True, kw_only=True)
class _CubeReveal:
    red: int
    green: int
    blue: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        cube_strs = [ss.strip() for ss in s.split(",")]
        counts = {"red": 0, "green": 0, "blue": 0}
        for cube_str in cube_strs:
            cube_count_str, cube_type_str = cube_str.split()
            counts[cube_type_str] = int(cube_count_str)
        return cls(**counts)


class Solution(SolutionAbstract, day=2):
    games: list[_Game]

    def _process_data(self, raw_data: list[str]) -> None:
        """
        Process day 02 data.
        """
        self.games = [_Game.from_str(row) for row in raw_data]

    def part_1(self) -> int:
        """
        Day 02 part 1 solution.
        """
        sum_ = 0
        for game in self.games:
            for reveal in game.reveals:
                if reveal.red > 12 or reveal.green > 13 or reveal.blue > 14:
                    break
            else:
                sum_ += game.id
        return sum_

    def part_2(self) -> int:
        """
        Day 02 part 2 solution.
        """
        sum_ = 0
        for game in self.games:
            red = max(reveal.red for reveal in game.reveals)
            green = max(reveal.green for reveal in game.reveals)
            blue = max(reveal.blue for reveal in game.reveals)
            sum_ += red * green * blue
        return sum_
