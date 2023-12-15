# pyright: reportMissingTypeStubs=false

from __future__ import annotations

import re

from utils import SolutionAbstract


class Solution(SolutionAbstract, day=15):
    strings: list[str]

    def _process_data(self, raw_data: list[str]) -> None:
        """
        Process day 15 data.
        """
        (raw_datum,) = raw_data
        self.strings = raw_datum.split(",")

    def part_1(self, *, visualize: bool = False) -> int:
        """
        Day 15 part 1 solution.
        """
        return sum(self._get_hash(s) for s in self.strings)

    def part_2(self, *, visualize: bool = False) -> int:
        """
        Day 15 part 2 solution.
        """
        boxes: list[dict[str, int]] = [{} for _ in range(256)]
        for s in self.strings:
            label, operation, value = re.split("([-=])", s)
            box_index = self._get_hash(label)
            box = boxes[box_index]
            match operation:
                case "-":
                    box.pop(label, None)
                case "=":
                    box[label] = int(value)
                case _:
                    raise ValueError(f'Invalid string "{s}"')
        return sum(
            box_number * slot_number * focal_length
            for box_number, box in enumerate(boxes, start=1)
            for slot_number, focal_length in enumerate(box.values(), start=1)
        )

    @staticmethod
    def _get_hash(s: str) -> int:
        val = 0
        for char in s:
            val += ord(char)
            val *= 17
            val %= 256
        return val
