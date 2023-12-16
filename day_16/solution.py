# pyright: reportMissingTypeStubs=false

from __future__ import annotations

from contextlib import suppress
from dataclasses import dataclass, field
from itertools import chain
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    type _Coord = complex
    type _Direction = complex
    type _LightState = tuple[_Coord, _Direction]

    type _ImmutableList[T] = tuple[T, ...]
    type _Immutable2DArray[T] = tuple[_ImmutableList[T], ...]


@dataclass(frozen=True, kw_only=True)
class _Contraption:
    data: _Immutable2DArray[str]
    row_count: int = field(init=False)
    col_count: int = field(init=False)
    next_state_cache: dict[_LightState, list[_LightState]] = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "row_count", len(self.data))
        object.__setattr__(self, "col_count", len(self.data[0]))
        object.__setattr__(self, "next_state_cache", {})

    def __getitem__(self, coord: _Coord) -> str:
        row = coord.imag
        col = coord.real
        if not row.is_integer() or not col.is_integer():
            raise ValueError("Non-integer rows and columns are not allowed")
        if row < 0 or col < 0:
            raise IndexError("Negative rows and columns are not allowed")
        return self.data[int(row)][int(col)]

    def get_next_states(self, curr_state: _LightState) -> list[_LightState]:
        with suppress(KeyError):
            return self.next_state_cache[curr_state]
        curr_coord, curr_dir = curr_state
        next_coord = curr_coord + curr_dir
        try:
            next_mirror = self[next_coord]
        except IndexError:
            self.next_state_cache[curr_state] = []
            return []
        next_states: list[_LightState]
        match next_mirror:
            case ".":
                next_states = [(next_coord, curr_dir)]
            case "/":
                next_dir = {1: -1j, -1j: 1, -1: 1j, 1j: -1}[curr_dir]
                next_states = [(next_coord, next_dir)]
            case "\\":
                next_dir = {1: 1j, 1j: 1, -1: -1j, -1j: -1}[curr_dir]
                next_states = [(next_coord, next_dir)]
            case "-":
                match curr_dir:
                    case 1 | -1:
                        next_states = [(next_coord, curr_dir)]
                    case 1j | -1j:
                        next_states = [(next_coord, -1), (next_coord, 1)]
                    case direction:
                        raise ValueError(f"Invalid direction {direction}")
            case "|":
                match curr_dir:
                    case 1j | -1j:
                        next_states = [(next_coord, curr_dir)]
                    case 1 | -1:
                        next_states = [(next_coord, -1j), (next_coord, 1j)]
                    case direction:
                        raise ValueError(f"Invalid direction {direction}")
            case item:
                raise ValueError(f"Invalid item {item}")
        self.next_state_cache[curr_state] = next_states
        return next_states


class Solution(SolutionAbstract, day=16):
    contraption: _Contraption

    def _process_data(self, raw_data: list[str]) -> None:
        """
        Process day 16 data.
        """
        self.contraption = _Contraption(data=tuple(map(tuple, raw_data)))

    def part_1(self, *, visualize: bool = False) -> int:
        """
        Day 16 part 1 solution.
        """
        return self._get_energized_tiles_count((-1, 1))

    def part_2(self, *, visualize: bool = False) -> int:
        """
        Day 16 part 2 solution.
        """
        row_count = self.contraption.row_count
        col_count = self.contraption.col_count
        starting_state_iter: chain[_LightState] = chain(
            ((-1 + r * 1j, 1) for r in range(row_count)),
            ((col_count + r * 1j, -1) for r in range(row_count)),
            ((c - 1j, 1j) for c in range(col_count)),
            ((c + row_count * 1j, -1j) for c in range(col_count)),
        )
        return max(
            self._get_energized_tiles_count(starting_state)
            for starting_state in starting_state_iter
        )

    def _get_energized_tiles_count(self, starting_state: _LightState) -> int:
        curr_states: set[_LightState] = {starting_state}
        seen_states: set[_LightState] = set()
        while curr_states:
            curr_states = {
                new_state
                for curr_state in curr_states
                for new_state in self.contraption.get_next_states(curr_state)
            }
            curr_states -= seen_states
            seen_states |= curr_states
        return len({coord for coord, _ in seen_states})
