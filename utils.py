# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, ClassVar


class SolutionAbstract(ABC):
    day: ClassVar[int] = 0

    def __init__(self) -> None:
        raw_data = self._get_raw_data()
        self.data = self._process_data(raw_data)

    def _get_input_path(self) -> Path:
        """"""
        return get_input_path(self.day)

    def _get_raw_data(self) -> list[str]:
        path = self._get_input_path()
        with path.open("r") as f:
            lines = [line.strip("\r\n") for line in f.readlines()]
        # Remove trailing empty lines
        while not lines[-1]:
            lines.pop()
        return lines

    @abstractmethod
    def _process_data(self, raw_data: list[str]) -> Any:
        """
        Process input data.
        """
        raise NotImplementedError()

    @abstractmethod
    def part_1(self) -> Any:
        """
        Part 1 solution.
        """
        raise NotImplementedError()

    @abstractmethod
    def part_2(self) -> Any:
        """
        Part 2 solution.
        """
        raise NotImplementedError()


def get_input_path(day: int) -> Path:
    """
    Get the path of the file the input data is downloaded into.
    Args:
        day (1..25): The day of AOC
    Returns:
        (pathlib.Path): Path of the input data file
    """
    if day not in range(1, 26):
        raise ValueError(f"Invalid day number {day}.")
    return Path(__file__).resolve().parent / f"day_{day:>02}" / "input.txt"
