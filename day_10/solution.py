# pyright: reportMissingTypeStubs=false

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from itertools import pairwise
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING

import numpy as np
from PIL import Image

from utils import SolutionAbstract

if TYPE_CHECKING:
    from types import TracebackType
    from typing import Self

    type _Coord = tuple[int, int]
    type _Color = tuple[int, int, int]
    type _GifFrameData = list[list[_Color]]


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


class _GifFrame:
    frame: _GifFrameData

    class Colors:
        UNVISITED: _Color = (111, 194, 118)
        VISITED: _Color = (0, 0, 0)
        PENDING: _Color = (255, 244, 155)
        LOOP: _Color = (251, 250, 245)
        RESULT: _Color = (236, 100, 75)

    pixel_size = 4

    def __init__(self, *, height: int, width: int) -> None:
        self.frame = [
            [self.Colors.VISITED] * width * self.pixel_size
            for _ in range(height * self.pixel_size)
        ]

    def set_color(self, *, row: int, col: int, color: _Color) -> None:
        ps = self.pixel_size
        for r in range(row * ps, row * ps + ps):
            for c in range(col * ps, col * ps + ps):
                self.frame[r][c] = color


class _Part2Visualizer:
    frame_paths: list[Path] = []
    temp_dir: TemporaryDirectory[str]
    temp_dir_path: Path
    can_run: bool

    gif_path = Path(__file__).resolve().parent / "part_2.gif"

    def __init__(self, *, dry_run: bool = False) -> None:
        self.frame_paths = []
        self.temp_dir = TemporaryDirectory()
        self.temp_dir_path = Path(self.temp_dir.name)
        self.can_run = not dry_run

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc: type[BaseException] | None,
        value: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.clean_up()

    def clean_up(self) -> None:
        self.temp_dir.cleanup()

    def add_frame(self, solver: _Part2Solver) -> None:
        if not self.can_run:
            return
        frame = _GifFrame(
            height=solver.transformed_field.row_count,
            width=solver.transformed_field.col_count,
        )
        for row, col in solver.unvisited_coords:
            frame.set_color(row=row, col=col, color=frame.Colors.UNVISITED)
        for row, col in solver.pending_coords:
            frame.set_color(row=row, col=col, color=frame.Colors.PENDING)
        for row, col in solver.transformed_field.loop_coords:
            frame.set_color(row=row, col=col, color=frame.Colors.LOOP)

        im = Image.fromarray(np.asarray(frame.frame, dtype=np.uint8))  # pyright: ignore[reportUnknownMemberType]
        path = self.temp_dir_path / f"{len(self.frame_paths):>07}.png"
        im.save(path)
        self.frame_paths.append(path)

    def add_final_frame(self, solver: _Part2Solver) -> None:
        if not self.can_run:
            return
        frame = _GifFrame(
            height=solver.transformed_field.row_count,
            width=solver.transformed_field.col_count,
        )
        for row, col in solver.pending_coords:
            frame.set_color(row=row, col=col, color=frame.Colors.PENDING)
        for row, col in solver.transformed_field.loop_coords:
            frame.set_color(row=row, col=col, color=frame.Colors.LOOP)
        for row, col in solver.unvisited_coords:
            color = (
                frame.Colors.RESULT if row % 2 and col % 2 else frame.Colors.UNVISITED
            )
            frame.set_color(row=row, col=col, color=color)

        im = Image.fromarray(np.asarray(frame.frame, dtype=np.uint8))  # pyright: ignore[reportUnknownMemberType]
        path = self.temp_dir_path / f"{len(self.frame_paths):>07}.png"
        im.save(path)
        self.frame_paths.append(path)

    def gen_gif(self) -> None:
        if not self.can_run:
            return
        ims = (Image.open(path) for path in self.frame_paths)
        im = next(ims)
        im.save(
            self.gif_path,
            save_all=True,
            append_images=ims,
            optimize=True,
            duration=1,
        )


class _Part2Solver:
    transformed_field: _TransformedField
    unvisited_coords: set[_Coord]
    pending_coords: set[_Coord]

    def __init__(self, transformed_field: _TransformedField) -> None:
        self.transformed_field = transformed_field
        self.unvisited_coords = {
            (row, col)
            for row in range(transformed_field.row_count)
            for col in range(transformed_field.col_count)
        } - transformed_field.loop_coords
        self.pending_coords = {(0, 0)}

    def run(self, *, visualize: bool = False) -> int:
        with _Part2Visualizer(dry_run=not visualize) as vis:
            loop_count = 0
            while self.pending_coords:
                if not loop_count % 1000:
                    print(f"\r\x1b[KFinished search loop #{loop_count}...", end="\r")
                vis.add_frame(self)
                curr_coord = self.pending_coords.pop()
                self.unvisited_coords.remove(curr_coord)
                self.pending_coords |= (
                    self.transformed_field.get_non_loop_neighbors(curr_coord)
                    & self.unvisited_coords
                )
                loop_count += 1
            vis.add_final_frame(self)
            vis.gen_gif()

        count_count = sum(
            1 for row, col in self.unvisited_coords if row % 2 and col % 2
        )
        return count_count


class Solution(SolutionAbstract, day=10):
    field: _Field

    def _process_data(self, raw_data: list[str]) -> None:
        """
        Process day 10 data.
        """
        self.field = _Field(pipes=[list(row) for row in raw_data])

    def part_1(self, *, visualize: bool = False) -> int:
        """
        Day 10 part 1 solution.
        """
        loop = self._get_loop()
        return len(loop) // 2

    def part_2(self, *, visualize: bool = False) -> int:
        """
        Day 10 part 2 solution.
        """
        transformed_loop = self._get_transformed_loop()
        transformed_field = _TransformedField(
            orig_field=self.field, transformed_loop=transformed_loop
        )
        return _Part2Solver(transformed_field).run(visualize=visualize)

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
