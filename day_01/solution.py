# pyright: reportMissingTypeStubs=false

from __future__ import annotations

from utils import SolutionAbstract


class Solution(SolutionAbstract, day=1):
    data: list[str]
    _WORD_MAP = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    def _process_data(self, raw_data: list[str]) -> None:
        """
        Process day 01 data.
        """
        self.data = raw_data

    def part_1(self, *, visualize: bool = False) -> int:
        """
        Day 01 part 1 solution.
        """
        sum_ = 0
        for row in self.data:
            first_digit = last_digit = None
            for char in row:
                if char.isdigit():
                    first_digit = char
                    break
            for char in reversed(row):
                if char.isdigit():
                    last_digit = char
                    break
            if first_digit is None or last_digit is None:
                raise ValueError(f"Cannot find digits in row {row}")
            sum_ += int(first_digit + last_digit)
        return sum_

    def part_2(self, *, visualize: bool = False) -> int:
        """
        Day 01 part 2 solution.
        """
        sum_ = 0
        for row in self.data:
            first_digit = None
            first_row = row
            while first_row:
                first_digit = self._part_2_check_starting_digit(first_row)
                if first_digit is not None:
                    break
                first_row = first_row[1:]
            last_digit = None
            last_row = row
            while last_row:
                last_digit = self._part_2_check_ending_digit(last_row)
                if last_digit is not None:
                    break
                last_row = last_row[:-1]
            if first_digit is None or last_digit is None:
                raise ValueError(f"Cannot find digits in row {row}")
            sum_ += int(first_digit + last_digit)
        return sum_

    @classmethod
    def _part_2_check_starting_digit(cls, s: str) -> None | str:
        """
        Check if the string has a starting digit for part 2
        """
        if s[0].isdigit():
            return s[0]
        for word, char in cls._WORD_MAP.items():
            if s.startswith(word):
                return char
        return None

    @classmethod
    def _part_2_check_ending_digit(cls, s: str) -> None | str:
        """
        Check if the string has a ending digit for part 2
        """
        if s[-1].isdigit():
            return s[-1]
        for word, char in cls._WORD_MAP.items():
            if s.endswith(word):
                return char
        return None
