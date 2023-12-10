# pyright: reportMissingTypeStubs=false

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from itertools import pairwise
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    type _Coord = tuple[int, int]
    from typing import Self


class _Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    WEST = "W"
    EAST = "E"


_D = _Direction


@dataclass(frozen=True, kw_only=True)
class _Walk:
    field: _Field
    coord: _Coord
    direction: None | _D

    def next(self) -> Self:
        row, col = self.coord
        match self.direction:
            case _D.NORTH:
                new_coord = (row - 1, col)
                new_pipe = self.field[new_coord]
                match new_pipe:
                    case "|":
                        new_direction = _D.NORTH
                    case "7":
                        new_direction = _D.WEST
                    case "F":
                        new_direction = _D.EAST
                    case "S":
                        new_direction = None
                    case _:
                        raise ValueError(
                            f"Invalid pipe when going north from {self.coord}"
                        )
            case _D.SOUTH:
                new_coord = (row + 1, col)
                new_pipe = self.field[new_coord]
                match new_pipe:
                    case "|":
                        new_direction = _D.SOUTH
                    case "J":
                        new_direction = _D.WEST
                    case "L":
                        new_direction = _D.EAST
                    case "S":
                        new_direction = None
                    case _:
                        raise ValueError(
                            f"Invalid pipe when going south from {self.coord}"
                        )
            case _D.WEST:
                new_coord = (row, col - 1)
                new_pipe = self.field[new_coord]
                match new_pipe:
                    case "-":
                        new_direction = _D.WEST
                    case "L":
                        new_direction = _D.NORTH
                    case "F":
                        new_direction = _D.SOUTH
                    case "S":
                        new_direction = None
                    case _:
                        raise ValueError(
                            f"Invalid pipe when going west from {self.coord}"
                        )
            case _D.EAST:
                new_coord = (row, col + 1)
                new_pipe = self.field[new_coord]
                match new_pipe:
                    case "-":
                        new_direction = _D.EAST
                    case "J":
                        new_direction = _D.NORTH
                    case "7":
                        new_direction = _D.SOUTH
                    case "S":
                        new_direction = None
                    case _:
                        raise ValueError(
                            f"Invalid pipe when going east from {self.coord}"
                        )
            case None:
                raise ValueError("Cannot walk without direction")

        return type(self)(field=self.field, coord=new_coord, direction=new_direction)


@dataclass(frozen=True, kw_only=True)
class _Field:
    pipes: list[list[str]]
    animal_coord: _Coord = field(init=False)
    row_count: int = field(init=False)
    col_count: int = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "animal_coord", self._get_animal_coord())
        object.__setattr__(self, "row_count", len(self.pipes))
        object.__setattr__(self, "col_count", len(self.pipes[0]))

    def __getitem__(self, coord: _Coord) -> str:
        row, col = coord
        return self.pipes[row][col]

    def _get_animal_coord(self) -> _Coord:
        for r, row in enumerate(self.pipes):
            for c, cell in enumerate(row):
                if cell == "S":
                    return (r, c)
        raise ValueError("Animal not found")

    def get_neighbor_coords(self, coord: _Coord) -> list[_Coord]:
        coords: list[_Coord] = []
        row, col = coord
        if row > 0:
            coords.append((row - 1, col))
        if row < self.row_count - 1:
            coords.append((row + 1, col))
        if col > 0:
            coords.append((row, col - 1))
        if col < self.col_count - 1:
            coords.append((row, col + 1))
        return coords

    def get_walk(self, *, coord: _Coord, direction: _D) -> _Walk:
        return _Walk(field=self, coord=coord, direction=direction)


class _TransformedField:
    loop_coords: set[_Coord]
    row_count: int
    col_count: int

    def __init__(self, *, orig_field: _Field, transformed_loop: list[_Coord]) -> None:
        self.loop_coords = set(transformed_loop)
        self.row_count = orig_field.row_count * 2 + 2
        self.col_count = orig_field.col_count * 2 + 2

    def get_non_loop_neighbors(self, coord: _Coord) -> set[_Coord]:
        coords: set[_Coord] = set()
        row, col = coord
        if row > 0:
            coords.add((row - 1, col))
        if row < self.row_count - 1:
            coords.add((row + 1, col))
        if col > 0:
            coords.add((row, col - 1))
        if col < self.col_count - 1:
            coords.add((row, col + 1))
        return coords - self.loop_coords


class Solution(SolutionAbstract, day=10):
    field: _Field

    def _process_data(self, raw_data: list[str]) -> None:
        """
        Process day 10 data.
        """
        self.field = _Field(pipes=[list(row) for row in raw_data])

    def part_1(self) -> int:
        """
        Day 10 part 1 solution.
        """
        loop = self._get_loop()
        return len(loop) // 2

    def part_2(self) -> int:
        """
        Day 10 part 2 solution.
        """
        transformed_loop = self._get_transformed_loop()
        transformed_field = _TransformedField(
            orig_field=self.field, transformed_loop=transformed_loop
        )
        unvisited_coords = {
            (row, col)
            for row in range(transformed_field.row_count)
            for col in range(transformed_field.col_count)
        } - transformed_field.loop_coords
        pending_coords: set[_Coord] = {(0, 0)}

        while pending_coords:
            curr_coord = pending_coords.pop()
            unvisited_coords.remove(curr_coord)
            pending_coords |= (
                transformed_field.get_non_loop_neighbors(curr_coord) & unvisited_coords
            )

        count_count = sum(1 for row, col in unvisited_coords if row % 2 and col % 2)
        return count_count

    def _get_animal_start_walks(self) -> tuple[_Walk, _Walk]:
        animal_row, animal_col = self.field.animal_coord
        walks: list[_Walk] = []
        if animal_row > 0:
            coord = (animal_row - 1, animal_col)
            match self.field[coord]:
                case "|":
                    walks.append(self.field.get_walk(coord=coord, direction=_D.NORTH))
                case "7":
                    walks.append(self.field.get_walk(coord=coord, direction=_D.WEST))
                case "F":
                    walks.append(self.field.get_walk(coord=coord, direction=_D.EAST))
                case _:
                    pass
        if animal_row < self.field.row_count - 1:
            coord = (animal_row + 1, animal_col)
            match self.field[coord]:
                case "|":
                    walks.append(self.field.get_walk(coord=coord, direction=_D.SOUTH))
                case "J":
                    walks.append(self.field.get_walk(coord=coord, direction=_D.WEST))
                case "L":
                    walks.append(self.field.get_walk(coord=coord, direction=_D.EAST))
                case _:
                    pass
        if animal_col > 0:
            coord = (animal_row, animal_col - 1)
            match self.field[coord]:
                case "-":
                    walks.append(self.field.get_walk(coord=coord, direction=_D.WEST))
                case "L":
                    walks.append(self.field.get_walk(coord=coord, direction=_D.NORTH))
                case "F":
                    walks.append(self.field.get_walk(coord=coord, direction=_D.SOUTH))
                case _:
                    pass
        if animal_col < self.field.col_count - 1:
            coord = (animal_row, animal_col + 1)
            match self.field[coord]:
                case "-":
                    walks.append(self.field.get_walk(coord=coord, direction=_D.EAST))
                case "J":
                    walks.append(self.field.get_walk(coord=coord, direction=_D.NORTH))
                case "7":
                    walks.append(self.field.get_walk(coord=coord, direction=_D.SOUTH))
                case _:
                    pass
        # This assumes that the data is constructed such that only 2 pipes connect to
        #   the animal's place. This is to validate that guess
        walk_1, walk_2 = walks
        return walk_1, walk_2

    def _get_loop(self) -> list[_Coord]:
        walk, _ = self._get_animal_start_walks()
        coords: list[_Coord] = [self.field.animal_coord]
        while walk.coord != self.field.animal_coord:
            coords.append(walk.coord)
            walk = walk.next()
        return coords

    def _get_transformed_loop(self) -> list[_Coord]:
        """
        Transform each (row, col) to (2*row+1, 2*col+1), and fill in the gaps
        """
        loop = self._get_loop()
        coords: list[_Coord] = []
        for (curr_row, curr_col), next_coord in pairwise(loop + [loop[0]]):
            trans_row = 2 * curr_row + 1
            trans_col = 2 * curr_col + 1
            # Transformed coord
            coords.append((trans_row, trans_col))
            # Fill gap
            if next_coord == (curr_row - 1, curr_col):
                coords.append((trans_row - 1, trans_col))
            elif next_coord == (curr_row + 1, curr_col):
                coords.append((trans_row + 1, trans_col))
            elif next_coord == (curr_row, curr_col - 1):
                coords.append((trans_row, trans_col - 1))
            elif next_coord == (curr_row, curr_col + 1):
                coords.append((trans_row, trans_col + 1))
            else:
                raise ValueError(
                    f"Invalid curr -> next coord {(curr_row, curr_col)} -> "
                    f"{next_coord}"
                )
        return coords
