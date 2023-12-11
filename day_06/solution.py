# pyright: reportMissingTypeStubs=false

from __future__ import annotations

import math
from dataclasses import dataclass
from math import prod

from utils import SolutionAbstract


@dataclass(frozen=True, kw_only=True)
class _Race:
    time: int
    distance: int

    def get_win_count(self) -> int:
        discriminant = self.time * self.time - 4 * self.distance
        if discriminant <= 0:
            return 0
        sd = math.sqrt(discriminant)
        t_min = math.floor((self.time - sd) / 2) + 1
        t_max = math.ceil((self.time + sd) / 2) - 1
        return t_max - t_min + 1


class Solution(SolutionAbstract, day=6):
    races: list[_Race]

    def _process_data(self, raw_data: list[str]) -> None:
        """
        Process day 06 data.
        """
        times_str, distances_str = raw_data
        times = map(int, times_str.split(":")[1].strip().split())
        distances = map(int, distances_str.split(":")[1].strip().split())
        self.races = [
            _Race(time=time, distance=distance)
            for time, distance in zip(times, distances, strict=True)
        ]

    def part_1(self, *, visualize: bool = False) -> int:
        """
        Day 06 part 1 solution.
        """
        return prod(race.get_win_count() for race in self.races)

    def part_2(self, *, visualize: bool = False) -> int:
        """
        Day 06 part 2 solution.
        """
        times_str, distances_str = self.raw_data
        time = int(times_str.split(":")[1].replace(" ", ""))
        distance = int(distances_str.split(":")[1].replace(" ", ""))
        race = _Race(time=time, distance=distance)
        return race.get_win_count()
