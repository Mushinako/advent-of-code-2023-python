from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
from functools import total_ordering
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self


@total_ordering
class _Card(Enum):
    ACE = 14
    KING = 13
    QUEEN = 12
    JACK = 11
    TEN = 10
    NINE = 9
    EIGHT = 8
    SEVEN = 7
    SIX = 6
    FIVE = 5
    FOUR = 4
    THREE = 3
    TWO = 2

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return self.value == __value.value
        return NotImplemented

    def __lt__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return self.value < __value.value
        return NotImplemented

    def __hash__(self) -> int:
        return self.value.__hash__()


_CARD_STR_MAP = {
    "A": _Card.ACE,
    "K": _Card.KING,
    "Q": _Card.QUEEN,
    "J": _Card.JACK,
    "T": _Card.TEN,
    "9": _Card.NINE,
    "8": _Card.EIGHT,
    "7": _Card.SEVEN,
    "6": _Card.SIX,
    "5": _Card.FIVE,
    "4": _Card.FOUR,
    "3": _Card.THREE,
    "2": _Card.TWO,
}


@total_ordering
class _HandType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIRS = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return self.value == __value.value
        return NotImplemented

    def __lt__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return self.value < __value.value
        return NotImplemented


@total_ordering
@dataclass(frozen=True, kw_only=True)
class Hand:
    hand: list[_Card]
    bid: int
    type: _HandType = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "type", self._get_type())

    def _get_type(self) -> _HandType:
        counts = sorted(Counter(self.hand).values(), reverse=True)
        match counts[0]:
            case 5:
                return _HandType.FIVE_OF_A_KIND
            case 4:
                return _HandType.FOUR_OF_A_KIND
            case 3:
                match counts[1]:
                    case 2:
                        return _HandType.FULL_HOUSE
                    case 1:
                        return _HandType.THREE_OF_A_KIND
                    case _:
                        raise ValueError(f"Invalid hand {self.hand}")
            case 2:
                match counts[1]:
                    case 2:
                        return _HandType.TWO_PAIRS
                    case 1:
                        return _HandType.ONE_PAIR
                    case _:
                        raise ValueError(f"Invalid hand {self.hand}")
            case 1:
                return _HandType.HIGH_CARD
            case _:
                raise ValueError(f"Invalid hand {self.hand}")

    @classmethod
    def from_row(cls, row: str) -> Self:
        hand_str, bid_str = row.split()
        return cls(hand=[_CARD_STR_MAP[char] for char in hand_str], bid=int(bid_str))

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return self.hand == __value.hand
        return NotImplemented

    def __lt__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            if self.type != __value.type:
                return self.type < __value.type
            return self.hand < __value.hand
        return NotImplemented
