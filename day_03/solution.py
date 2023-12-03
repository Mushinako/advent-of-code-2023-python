# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    from collections.abc import Iterable

    type _Coord = tuple[int, int]


@dataclass(frozen=True, kw_only=True)
class _Schematic:
    data: list[list[str]]
    row_count: int = field(init=False)
    col_count: int = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "row_count", len(self.data))
        object.__setattr__(self, "col_count", len(self.data[0]))

    def __getitem__(self, index: _Coord) -> str:
        row, col = index
        return self.data[row][col]

    def iter_cells(self) -> Iterable[tuple[_Coord, str]]:
        for r, row in enumerate(self.data):
            for c, cell in enumerate(row):
                yield (r, c), cell

    def iter_adjacent_coords(self, coord: _Coord) -> Iterable[_Coord]:
        row, col = coord
        for r in range(max(0, row - 1), min(self.row_count, row + 2)):
            for c in range(max(0, col - 1), min(self.col_count, col + 2)):
                if r != row or c != col:
                    yield r, c

    def get_number(self, coord: _Coord) -> None | tuple[list[_Coord], int]:
        row, col = coord
        if not self[row, col].isdigit():
            return None
        c_start = col
        while c_start > 0:
            if not self[row, c_start - 1].isdigit():
                break
            c_start -= 1
        c_end = col + 1
        while c_end < self.col_count:
            if not self[row, c_end].isdigit():
                break
            c_end += 1
        return [(row, c) for c in range(c_start, c_end)], int(
            "".join(self.data[row][c_start:c_end])
        )

    def get_adjacent_numbers(self, coord: _Coord) -> list[int]:
        """
        Note: the numbers are unordered
        """
        adjacent_numbers: list[int] = []
        coords_to_check = set(self.iter_adjacent_coords(coord))
        while coords_to_check:
            check_coord, *_ = coords_to_check
            num_result = self.get_number(check_coord)
            if num_result is None:
                coords_to_check.discard(check_coord)
                continue
            covered_coords, num = num_result
            coords_to_check.difference_update(covered_coords)
            adjacent_numbers.append(num)
        return adjacent_numbers


class Solution(SolutionAbstract):
    day = 3
    data: _Schematic

    def _process_data(self, raw_data: list[str]) -> _Schematic:
        """
        Process day 03 data.
        """
        return _Schematic(data=[list(row) for row in raw_data])

    def part_1(self) -> int:
        """
        Day 03 part 1 solution.
        """
        sum_ = 0
        for coord, cell in self.data.iter_cells():
            if cell.isdigit() or cell == ".":
                continue
            adjacent_numbers = self.data.get_adjacent_numbers(coord)
            sum_ += sum(adjacent_numbers)
        return sum_

    def part_2(self) -> int:
        """
        Day 03 part 2 solution.
        """
        sum_ = 0
        for coord, cell in self.data.iter_cells():
            if cell != "*":
                continue
            adjacent_numbers = self.data.get_adjacent_numbers(coord)
            if len(adjacent_numbers) != 2:
                continue
            sum_ += adjacent_numbers[0] * adjacent_numbers[1]
        return sum_
