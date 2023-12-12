# pyright: reportMissingTypeStubs=false

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import cache
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    from typing import Self


@dataclass(frozen=True, kw_only=True)
class _Record:
    springs_str: str
    damaged_spring_group_sizes: tuple[int, ...]

    @classmethod
    def from_row(cls, row: str) -> Self:
        springs_str, damaged_spring_group_sizes_str = row.split()
        damaged_spring_group_sizes = tuple(
            map(int, damaged_spring_group_sizes_str.split(","))
        )
        return cls(
            springs_str=springs_str,
            damaged_spring_group_sizes=damaged_spring_group_sizes,
        )

    def get_possibilities_count(self) -> int:
        return self._get_possibilities_count(
            springs_str=self.springs_str.strip("."),
            damaged_spring_group_sizes=self.damaged_spring_group_sizes,
        )

    @classmethod
    @cache
    def _get_possibilities_count(
        cls, *, springs_str: str, damaged_spring_group_sizes: tuple[int, ...]
    ) -> int:
        springs_str = springs_str.lstrip(".")
        # Check terminating conditions
        if not springs_str:
            #   There should be no more damaged spring group sizes left
            return int(not damaged_spring_group_sizes)
        if not damaged_spring_group_sizes:
            #   All springs must be operational
            return int("#" not in springs_str)
        #   Make sure the springs can hold required damaged spring group sizes
        if (
            len(springs_str)
            < sum(damaged_spring_group_sizes) + len(damaged_spring_group_sizes) - 1
        ):
            return 0
        #   Make sure there are enough damaged spring group sizes to account for damaged
        #     spring separations
        known_springs_str = "".join(spring for spring in springs_str if spring != "?")
        damaged_spring_groups_separation_count = len(
            re.split(r"\.+", known_springs_str.strip("."))
        )
        if damaged_spring_groups_separation_count > len(damaged_spring_group_sizes):
            return 0

        # If first spring is damaged...
        #   Shouldn't have operational springs in range
        first_damaged_spring_group_size = damaged_spring_group_sizes[0]
        proposed_damaged_springs = list(springs_str[:first_damaged_spring_group_size])
        try:
            operational_index = proposed_damaged_springs.index(".")
        except ValueError:
            pass
        else:
            #   Damaged spring shoudn't be before operational spring in the section
            if "#" in proposed_damaged_springs[:operational_index]:
                return 0
            #   All springs before the operational spring are also undamaged
            return cls._get_possibilities_count(
                springs_str=springs_str[operational_index + 1 :],
                damaged_spring_group_sizes=damaged_spring_group_sizes,
            )
        #   Shouldn't be followed by a damaged spring
        if (
            len(springs_str) > first_damaged_spring_group_size
            and springs_str[first_damaged_spring_group_size] == "#"
        ):
            first_spring_damaged_possibilities_count = 0
        else:
            first_spring_damaged_possibilities_count = cls._get_possibilities_count(
                springs_str=springs_str[first_damaged_spring_group_size + 1 :],
                damaged_spring_group_sizes=damaged_spring_group_sizes[1:],
            )

        # If first spring is operational...
        if springs_str[0] == "#":
            first_spring_operational_possibilities_count = 0
        # Starts with `?`
        else:
            first_spring_operational_possibilities_count = cls._get_possibilities_count(
                springs_str=springs_str[1:],
                damaged_spring_group_sizes=damaged_spring_group_sizes,
            )
        return (
            first_spring_damaged_possibilities_count
            + first_spring_operational_possibilities_count
        )


@dataclass(frozen=True, kw_only=True)
class _UnfoldedRecord(_Record):
    @classmethod
    def from_row(cls, row: str) -> Self:
        springs_str, damaged_spring_group_sizes_str = row.split()
        springs_str = "?".join([springs_str] * 5)
        damaged_spring_group_sizes = tuple(
            map(int, damaged_spring_group_sizes_str.split(",") * 5)
        )
        return cls(
            springs_str=springs_str,
            damaged_spring_group_sizes=damaged_spring_group_sizes,
        )

    @classmethod
    def from_folded_record(cls, record: _Record) -> Self:
        springs_str = "?".join([record.springs_str] * 5)
        damaged_spring_group_sizes = record.damaged_spring_group_sizes * 5
        return cls(
            springs_str=springs_str,
            damaged_spring_group_sizes=damaged_spring_group_sizes,
        )


class Solution(SolutionAbstract, day=12):
    records: list[_Record]

    def _process_data(self, raw_data: list[str]) -> None:
        """
        Process day 12 data.
        """
        self.records = [_Record.from_row(row) for row in raw_data]

    def part_1(self, *, visualize: bool = False) -> int:
        """
        Day 12 part 1 solution.
        """
        return sum(record.get_possibilities_count() for record in self.records)

    def part_2(self, *, visualize: bool = False) -> int:
        """
        Day 12 part 2 solution.
        """
        unfolded_records = map(_UnfoldedRecord.from_folded_record, self.records)
        return sum(record.get_possibilities_count() for record in unfolded_records)
