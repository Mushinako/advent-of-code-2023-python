# pyright: reportMissingTypeStubs=false

from __future__ import annotations

from dataclasses import dataclass, field
from functools import cache
from itertools import product

from utils import SolutionAbstract


@dataclass(frozen=True, kw_only=True)
class _Pattern:
    data: tuple[tuple[str, ...], ...]
    transposed_data: tuple[tuple[str, ...], ...] = field(init=False)
    row_count: int = field(init=False)
    col_count: int = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "transposed_data", tuple(map(tuple, zip(*self.data, strict=True)))
        )
        object.__setattr__(self, "row_count", len(self.data))
        object.__setattr__(self, "col_count", len(self.data[0]))

    def get_reflection_score(self, *, exclude: None | int = None) -> None | int:
        row_exclude = col_exclude = None
        if exclude is not None:
            if exclude % 100:
                col_exclude = exclude
            else:
                row_exclude = exclude // 100
        row = self._get_reflection_row(exclude=row_exclude)
        if row is not None:
            return 100 * row
        col = self._get_reflection_col(exclude=col_exclude)
        if col is not None:
            return col

    def _get_reflection_row(self, *, exclude: None | int = None) -> None | int:
        return self._get_hori_reflection_index(self.data, exclude=exclude)

    def _get_reflection_col(self, *, exclude: None | int = None) -> None | int:
        return self._get_hori_reflection_index(self.transposed_data, exclude=exclude)

    @staticmethod
    @cache
    def _get_hori_reflection_index(
        pattern_data: tuple[tuple[str, ...], ...], *, exclude: None | int = None
    ) -> None | int:
        for i in range(1, len(pattern_data)):
            if i == exclude:
                continue
            top = pattern_data[:i]
            bot = pattern_data[i:]
            for l1, l2 in zip(top[::-1], bot, strict=False):
                if l1 != l2:
                    break
            else:
                return i


class Solution(SolutionAbstract, day=13):
    patterns: list[_Pattern]

    def _process_data(self, raw_data: list[str]) -> None:
        """
        Process day 13 data.
        """
        patterns: list[_Pattern] = []
        pattern_data: list[tuple[str, ...]] = []
        for row in raw_data + [""]:
            if not row:
                patterns.append(_Pattern(data=tuple(pattern_data)))
                pattern_data = []
            else:
                pattern_data.append(tuple(row))
        assert not pattern_data
        self.patterns = patterns

    def part_1(self, *, visualize: bool = False) -> int:
        """
        Day 13 part 1 solution.
        """
        total = 0
        for pattern in self.patterns:
            score = pattern.get_reflection_score()
            if score is None:
                raise ValueError("Cannot find a reflection")
            total += score
        return total

    def part_2(self, *, visualize: bool = False) -> int:
        """
        Day 13 part 2 solution.
        """
        total = 0
        for pattern in self.patterns:
            score = pattern.get_reflection_score()
            if score is None:
                raise ValueError("Cannot find a reflection")
            for change_row_index, change_col_index in product(
                range(pattern.row_count), range(pattern.col_count)
            ):
                new_pattern_data = tuple(
                    tuple(
                        ("#" if cell == "." else ".") if c == change_col_index else cell
                        for c, cell in enumerate(row)
                    )
                    if r == change_row_index
                    else row
                    for r, row in enumerate(pattern.data)
                )
                new_pattern = _Pattern(data=new_pattern_data)
                new_score = new_pattern.get_reflection_score(exclude=score)
                if new_score is None:
                    continue
                assert new_score != score
                total += new_score
                break
            else:
                raise ValueError("Cannot find a reflection for all changes")
        return total
