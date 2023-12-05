# pyright: reportMissingTypeStubs=false

from __future__ import annotations

from bisect import bisect_left, bisect_right
from dataclasses import dataclass, field
from itertools import batched, chain
from operator import attrgetter
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    from typing import Self


@dataclass(frozen=True, kw_only=True)
class _AlmanacMapRange:
    """
    A range in the alamanic mapping, corresponds to a row
    """

    src_start: int
    dest_start: int
    length: int

    @classmethod
    def from_row(cls, row: str) -> Self:
        dest_start, src_start, length = map(int, row.strip().split())
        return cls(src_start=src_start, dest_start=dest_start, length=length)


class _AlmanacMap:
    """
    Attributes:
        forward_ranges (list[_AlmanacMapRange]):
            All ranges, sorted by `src_start`. This is for easier bisecting when getting
            `dest` value from `src` value
        backward_ranges (list[_AlmanacMapRange]):
            All ranges, sorted by `dest_start`. This is for easier bisecting when
            getting `src` value from `dest` value
        src_starts (list[int]):
            All of the `src_start` from all ranges, sorted
        dest_starts (list[int]):
            All of the `dest_start` from all ranges, sorted
    """

    forward_ranges: list[_AlmanacMapRange]
    backward_ranges: list[_AlmanacMapRange]
    src_starts: list[int]
    dest_starts: list[int]

    def __init__(self, ranges: list[_AlmanacMapRange]) -> None:
        self.forward_ranges = sorted(ranges, key=attrgetter("src_start"))
        self.backward_ranges = sorted(ranges, key=attrgetter("dest_start"))
        self.src_starts = [range_.src_start for range_ in self.forward_ranges]
        self.dest_starts = [range_.dest_start for range_ in self.backward_ranges]

    @classmethod
    def from_rows(cls, rows: list[str]) -> Self:
        return cls(ranges=[_AlmanacMapRange.from_row(row) for row in rows])

    def forward_get(self, key: int) -> int:
        """
        Get `dest` value from `src` value
        """
        return self._get(
            key=key,
            ranges=self.forward_ranges,
            src_field="src_start",
            dest_field="dest_start",
        )

    def backward_get(self, key: int) -> int:
        """
        Get `src` value from `dest` value
        """
        return self._get(
            key=key,
            ranges=self.backward_ranges,
            src_field="dest_start",
            dest_field="src_start",
        )

    @staticmethod
    def _get(
        *, key: int, ranges: list[_AlmanacMapRange], src_field: str, dest_field: str
    ) -> int:
        """
        Shared logics for `forward_get` and `backward_get`
        """
        index = bisect_right(ranges, key, key=attrgetter(src_field)) - 1
        range_ = ranges[index]
        offset = key - getattr(range_, src_field)
        if 0 <= offset < range_.length:
            return getattr(range_, dest_field) + offset
        return key


@dataclass(frozen=True, kw_only=True)
class _Almanac:
    """
    Attributes:
        seed_starts (list[int]):
            All seed values that correspond to a `src_start` in **any** of the mappings,
            sorted for easier bisecting. Values from non-seed categories are translated
            back to seed numbers via `backward_get`
    """

    seed_soil_map: _AlmanacMap
    soil_fert_map: _AlmanacMap
    fert_water_map: _AlmanacMap
    water_light_map: _AlmanacMap
    light_temp_map: _AlmanacMap
    temp_hum_map: _AlmanacMap
    hum_loc_map: _AlmanacMap

    seed_starts: list[int] = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "seed_starts", self._get_seed_starts())

    def _get_seed_starts(self) -> list[int]:
        """
        Get all seed values that correspond to a `src_start` in any of the mappings,
          sorted
        """
        hum_starts = self.hum_loc_map.src_starts
        temp_starts = chain(
            map(self.temp_hum_map.backward_get, hum_starts),
            self.temp_hum_map.src_starts,
        )
        light_starts = chain(
            map(self.light_temp_map.backward_get, temp_starts),
            self.light_temp_map.src_starts,
        )
        water_starts = chain(
            map(self.water_light_map.backward_get, light_starts),
            self.water_light_map.src_starts,
        )
        fert_starts = chain(
            map(self.fert_water_map.backward_get, water_starts),
            self.fert_water_map.src_starts,
        )
        soil_starts = chain(
            map(self.soil_fert_map.backward_get, fert_starts),
            self.soil_fert_map.src_starts,
        )
        seed_starts = chain(
            map(self.seed_soil_map.backward_get, soil_starts),
            self.seed_soil_map.src_starts,
        )
        # No need to consider a lower bound. That will be taken care of by the
        #   candidate ranges
        return sorted(set(seed_starts))

    def __getitem__(self, seed: int) -> int:
        return self.get_seed_loc(seed)

    def get_seed_loc(self, seed: int) -> int:
        """
        Get location number corresponding to the seed number
        """
        soil = self.seed_soil_map.forward_get(seed)
        fert = self.soil_fert_map.forward_get(soil)
        water = self.fert_water_map.forward_get(fert)
        light = self.water_light_map.forward_get(water)
        temp = self.light_temp_map.forward_get(light)
        hum = self.temp_hum_map.forward_get(temp)
        return self.hum_loc_map.forward_get(hum)

    def get_range_seed_candidates(
        self, *, seed_start: int, seed_length: int
    ) -> list[int]:
        """
        Get a list of possible seed numbers that may produce the lowest location number
        """
        min_index = bisect_left(self.seed_starts, seed_start)
        max_index = bisect_right(self.seed_starts, seed_start + seed_length - 1)
        range_seed_starts = set(self.seed_starts[min_index : max_index + 1])
        range_seed_starts.add(seed_start)
        return sorted(range_seed_starts)


class Solution(SolutionAbstract, day=5):
    seed_configs: list[int]
    almanac: _Almanac

    def _process_data(self, raw_data: list[str]) -> None:
        """
        Process day 05 data.
        """
        data_iter = iter(raw_data)
        self.seed_configs = list(
            map(int, next(data_iter).split(":")[1].strip().split())
        )

        def get_section_rows() -> list[str]:
            next(data_iter)
            next(data_iter)
            rows: list[str] = []
            for row in data_iter:
                if row:
                    rows.append(row)
                else:
                    break
            return rows

        seed_soil_rows = get_section_rows()
        soil_fert_rows = get_section_rows()
        fert_water_rows = get_section_rows()
        water_light_rows = get_section_rows()
        light_temp_rows = get_section_rows()
        temp_hum_rows = get_section_rows()
        hum_loc_rows = get_section_rows()

        self.almanac = _Almanac(
            seed_soil_map=_AlmanacMap.from_rows(seed_soil_rows),
            soil_fert_map=_AlmanacMap.from_rows(soil_fert_rows),
            fert_water_map=_AlmanacMap.from_rows(fert_water_rows),
            water_light_map=_AlmanacMap.from_rows(water_light_rows),
            light_temp_map=_AlmanacMap.from_rows(light_temp_rows),
            temp_hum_map=_AlmanacMap.from_rows(temp_hum_rows),
            hum_loc_map=_AlmanacMap.from_rows(hum_loc_rows),
        )

    def part_1(self) -> int:
        """
        Day 05 part 1 solution.
        """
        return min(self.almanac[seed] for seed in self.seed_configs)

    def part_2(self) -> int:
        """
        Day 05 part 2 solution.
        """
        return min(
            self.almanac[seed]
            for seed_start, seed_length in batched(self.seed_configs, 2)
            for seed in self.almanac.get_range_seed_candidates(
                seed_start=seed_start, seed_length=seed_length
            )
        )
