# pyright: reportMissingTypeStubs=false

from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass
from itertools import batched
from operator import attrgetter
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    from typing import Self


@dataclass(frozen=True, kw_only=True, order=True)
class _AlmanacMapRange:
    src_start: int
    dest_start: int
    length: int

    @classmethod
    def from_row(cls, row: str) -> Self:
        dest_start, src_start, length = map(int, row.strip().split())
        return cls(src_start=src_start, dest_start=dest_start, length=length)


@dataclass(frozen=True, kw_only=True)
class _AlmanacMap:
    ranges: list[_AlmanacMapRange]

    def __post_init__(self) -> None:
        self.ranges.sort()

    @classmethod
    def from_rows(cls, rows: list[str]) -> Self:
        return cls(ranges=[_AlmanacMapRange.from_row(row) for row in rows])

    def __getitem__(self, key: int) -> int:
        index = bisect_right(self.ranges, key, key=attrgetter("src_start"))
        range_ = self.ranges[index - 1]
        offset = key - range_.src_start
        if 0 <= offset < range_.length:
            return range_.dest_start + offset
        return key


@dataclass(frozen=True, kw_only=True)
class _Almanac:
    seed_soil_map: _AlmanacMap
    soil_fert_map: _AlmanacMap
    fert_water_map: _AlmanacMap
    water_light_map: _AlmanacMap
    light_temp_map: _AlmanacMap
    temp_hum_map: _AlmanacMap
    hum_loc_map: _AlmanacMap

    def get_seed_loc(self, seed: int) -> int:
        soil = self.seed_soil_map[seed]
        fert = self.soil_fert_map[soil]
        water = self.fert_water_map[fert]
        light = self.water_light_map[water]
        temp = self.light_temp_map[light]
        hum = self.temp_hum_map[temp]
        return self.hum_loc_map[hum]


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
        return min(self.almanac.get_seed_loc(seed) for seed in self.seed_configs)

    def part_2(self) -> int:
        """
        Day 05 part 2 solution.
        """
        min_loc = None
        for seed_start, seed_length in batched(self.seed_configs, 2):
            print(f"Processing {seed_start} {seed_length}")
            for i, seed in enumerate(range(seed_start, seed_start + seed_length)):
                if not i % 1_000_000:
                    print(f"  Processed {i} seeds")
                loc = self.almanac.get_seed_loc(seed)
                if min_loc is None:
                    min_loc = loc
                else:
                    min_loc = min(min_loc, loc)
        assert min_loc is not None
        return min_loc
