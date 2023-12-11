# pyright: reportMissingTypeStubs=false

from __future__ import annotations

from dataclasses import dataclass

from utils import SolutionAbstract


@dataclass(frozen=True, kw_only=True)
class _History:
    values: list[int]

    def predict_next_value(self) -> int:
        values = self.values
        last_value_history = [values[-1]]
        while any(value for value in values):
            values = self._get_diffs(values)
            last_value_history.append(values[-1])
        return sum(last_value_history)

    def predict_previous_value(self) -> int:
        values = self.values
        first_value_history = [values[0]]
        while any(value for value in values):
            values = self._get_diffs(values)
            first_value_history.append(values[0])
        return sum(first_value_history[::2]) - sum(first_value_history[1::2])

    @staticmethod
    def _get_diffs(values: list[int]) -> list[int]:
        return [values[i + 1] - values[i] for i in range(len(values) - 1)]


class Solution(SolutionAbstract, day=9):
    histories: list[_History]

    def _process_data(self, raw_data: list[str]) -> None:
        """
        Process day 09 data.
        """
        self.histories = [
            _History(values=list(map(int, row.split()))) for row in raw_data
        ]

    def part_1(self, *, visualize: bool = False) -> int:
        """
        Day 09 part 1 solution.
        """
        return sum(history.predict_next_value() for history in self.histories)

    def part_2(self, *, visualize: bool = False) -> int:
        """
        Day 09 part 2 solution.
        """
        return sum(history.predict_previous_value() for history in self.histories)
