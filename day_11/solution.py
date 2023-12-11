# pyright: reportMissingTypeStubs=false

from __future__ import annotations

from bisect import bisect_left, bisect_right
from dataclasses import dataclass, field
from itertools import combinations
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    type _Coord = tuple[int, int]


class _DistanceCalculator:
    image: _Image
    expansion_size: int

    def __init__(self, *, image: _Image, expansion_size: int) -> None:
        self.image = image
        self.expansion_size = expansion_size

    def get_distance(self, coord_1: _Coord, coord_2: _Coord) -> int:
        row_diff = self._get_diff(
            occupied=self.image.occupied_rows, val_1=coord_1[0], val_2=coord_2[0]
        )
        col_diff = self._get_diff(
            occupied=self.image.occupied_cols, val_1=coord_1[1], val_2=coord_2[1]
        )
        return row_diff + col_diff

    def _get_diff(self, *, occupied: list[int], val_1: int, val_2: int) -> int:
        val_low = min(val_1, val_2)
        val_high = max(val_1, val_2)
        val_low_occupied_index = bisect_right(occupied, val_low)
        val_high_occupied_index = bisect_left(occupied, val_high)
        val_gap = val_high - val_low - 1
        occupied_count = val_high_occupied_index - val_low_occupied_index
        return (val_gap - occupied_count) * self.expansion_size + occupied_count + 1


@dataclass(frozen=True, kw_only=True)
class _Image:
    galaxy_coords: list[_Coord]
    occupied_rows: list[int] = field(init=False)
    occupied_cols: list[int] = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "occupied_rows", sorted(set(r for r, _ in self.galaxy_coords))
        )
        object.__setattr__(
            self, "occupied_cols", sorted(set(c for _, c in self.galaxy_coords))
        )


class Solution(SolutionAbstract, day=11):
    image: _Image

    def _process_data(self, raw_data: list[str]) -> None:
        """
        Process day 11 data.
        """
        galaxy_coords: list[_Coord] = [
            (r, c)
            for r, row in enumerate(raw_data)
            for c, cell in enumerate(row)
            if cell == "#"
        ]
        self.image = _Image(galaxy_coords=galaxy_coords)

    def part_1(self, *, visualize: bool = False) -> int:
        """
        Day 11 part 1 solution.
        """
        calculator = _DistanceCalculator(image=self.image, expansion_size=2)
        return sum(
            calculator.get_distance(coord_1, coord_2)
            for coord_1, coord_2 in combinations(self.image.galaxy_coords, r=2)
        )

    def part_2(self, *, visualize: bool = False) -> int:
        """
        Day 11 part 2 solution.
        """
        calculator = _DistanceCalculator(image=self.image, expansion_size=1000000)
        return sum(
            calculator.get_distance(coord_1, coord_2)
            for coord_1, coord_2 in combinations(self.image.galaxy_coords, r=2)
        )
