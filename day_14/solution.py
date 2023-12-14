# pyright: reportMissingTypeStubs=false

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    from typing import Self

    type _Tuple[T] = tuple[T, ...]
    type _2DTuple[T] = tuple[_Tuple[T], ...]


@dataclass(frozen=True, kw_only=True)
class _Platform:
    data: _2DTuple[str]

    @staticmethod
    @cache
    def _transpose(data: _2DTuple[str]) -> _2DTuple[str]:
        return tuple(map(tuple, zip(*data, strict=True)))

    @staticmethod
    @cache
    def _reverse(data: _2DTuple[str]) -> _2DTuple[str]:
        return tuple(row[::-1] for row in data)

    @staticmethod
    @cache
    def _roll_row(row: _Tuple[str]) -> _Tuple[str]:
        row_str = "".join(row)
        segments = row_str.split("#")
        rolled_segment_gen = (
            "O" * (c := segment.count("O")) + "." * (len(segment) - c)
            for segment in segments
        )
        return tuple("#".join(rolled_segment_gen))

    @classmethod
    @cache
    def _roll_rows(cls, data: _2DTuple[str]) -> _2DTuple[str]:
        return tuple(cls._roll_row(row) for row in data)

    @cache
    def roll_north(self) -> Self:
        converted_data = self._transpose(self.data)
        rolled_converted_data = self._roll_rows(converted_data)
        rolled_data = self._transpose(rolled_converted_data)
        return type(self)(data=rolled_data)

    @cache
    def roll_south(self) -> Self:
        converted_data = self._reverse(self._transpose(self.data))
        rolled_converted_data = self._roll_rows(converted_data)
        rolled_data = self._transpose(self._reverse(rolled_converted_data))
        return type(self)(data=rolled_data)

    @cache
    def roll_west(self) -> Self:
        converted_data = self.data
        rolled_converted_data = self._roll_rows(converted_data)
        rolled_data = rolled_converted_data
        return type(self)(data=rolled_data)

    @cache
    def roll_east(self) -> Self:
        converted_data = self._reverse(self.data)
        rolled_converted_data = self._roll_rows(converted_data)
        rolled_data = self._reverse(rolled_converted_data)
        return type(self)(data=rolled_data)

    @cache
    def spin_cycle(self) -> Self:
        return self.roll_north().roll_west().roll_south().roll_east()

    def get_north_load(self) -> int:
        return sum(
            i * sum(1 for cell in row if cell == "O")
            for i, row in enumerate(reversed(self.data), start=1)
        )


class Solution(SolutionAbstract, day=14):
    platform: _Platform

    def _process_data(self, raw_data: list[str]) -> None:
        """
        Process day 14 data.
        """
        self.platform = _Platform(data=tuple(tuple(row) for row in raw_data))

    def part_1(self, *, visualize: bool = False) -> int:
        """
        Day 14 part 1 solution.
        """
        rolled_platform = self.platform.roll_north()
        return rolled_platform.get_north_load()

    def part_2(self, *, visualize: bool = False) -> int:
        """
        Day 14 part 2 solution.
        """
        orig_loop_count = 1_000_000_000
        rolled_platform = self.platform
        seen_data_map: dict[_Platform, int] = {self.platform: 0}
        for i in range(orig_loop_count):
            rolled_platform = rolled_platform.spin_cycle()
            if rolled_platform in seen_data_map:
                break
            seen_data_map[rolled_platform] = i
        else:
            # Worst case, do all 1 billion loops
            return rolled_platform.get_north_load()
        prev_i = seen_data_map[rolled_platform]
        loop_size = i - prev_i
        actual_loop_count = (orig_loop_count - prev_i) % loop_size + prev_i
        rolled_platform = list(seen_data_map)[actual_loop_count]
        return rolled_platform.get_north_load()
