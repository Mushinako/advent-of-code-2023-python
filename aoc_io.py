# pyright: reportMissingTypeStubs=false
"""
Get input from and submit answer to AOC
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from string import Template
from time import sleep
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

import requests
import yaml
from bs4 import BeautifulSoup
from colorama import Fore, init

from utils import get_input_path

if TYPE_CHECKING:
    from typing import Literal, Optional

init(autoreset=True)

_CONFIG_PATH = Path(__file__).resolve().parent / "config.yml"
with _CONFIG_PATH.open("r") as f:
    _CONFIG = yaml.safe_load(f)

DATA_URL = Template("https://adventofcode.com/2022/day/${day}/input")
ANSWER_URL = Template("https://adventofcode.com/2022/day/${day}/answer")

_COOKIES = _CONFIG["cookies"]

_DAY_CHOICES = set(range(1, 26))
_LEVEL_CHOICES = {1, 2}


def download_input(day: int, input_path: Optional[Path] = None) -> None:
    """
    Download input from AOC website.
    Args:
        day        (1..25)       : The day of AOC
        input_path (pathlib.Path): Path of file to write input to
    """
    if day not in _DAY_CHOICES:
        raise ValueError(f"{day=} is not in range 1..25")
    # One extra second just to be sure
    target_time_est = datetime(2022, 12, day, 0, 0, 1, tzinfo=ZoneInfo("EST"))
    target_time_local = datetime.fromtimestamp(target_time_est.timestamp())

    while (now := datetime.now()) < target_time_local:
        diff = target_time_local - now
        seconds = max(diff.days * 86400 + diff.seconds, 0)
        print(f"\r\x1b[K{seconds} seconds until problem opens. Waiting...", end="")
        sleep(1)
    print("\r\x1b[K", end="")

    for _ in range(3):
        with requests.get(DATA_URL.substitute(day=day), cookies=_COOKIES) as response:
            data = response.content
            if not response.ok:
                print(Fore.RED + data.decode("utf-8").strip())
                sleep(5)
                continue
            break
    else:
        raise ConnectionError("Download failed!")

    print(
        Fore.GREEN
        + f"Got input with {len(data)} characters and {len(data.splitlines())} lines"
    )
    if input_path is None:
        input_path = get_input_path(day)
    with input_path.open("wb") as input_fp:
        input_fp.write(data)


def submit_output(day: int, part: Literal[1, 2], answer: str | int) -> None:
    """
    Upload solution to AOC website
    Args:
        day    (1..25)    : The day of AOC
        part   (1, 2)     : Whether the submission is for part 1 or 2
        answer (str | int): Answer to be submitted
    Returns:
        (str): Success/failure string, with coloring
    """
    if day not in _DAY_CHOICES:
        raise ValueError(f"{day=} is not in range 1..25")
    if part not in _LEVEL_CHOICES:
        raise ValueError(f"{part=} is not 1 or 2")

    for _ in range(3):
        with requests.post(
            ANSWER_URL.substitute(day=day),
            {"level": part, "answer": answer},
            cookies=_COOKIES,
        ) as response:
            data = response.content
            if not response.ok:
                print(Fore.RED + data.decode("utf-8").strip())
                sleep(1)
                continue
            break
    else:
        raise ConnectionError("Failed to submit response.")

    html = BeautifulSoup(data, "html.parser")
    try:
        response_text: str = html.article.p.text
    except AttributeError as err:
        raise ValueError(f"Unknown response html: {data}") from err
    if response_text.startswith("You don't"):
        print(Fore.YELLOW + response_text)
    elif response_text.startswith("That's the"):
        print(Fore.GREEN + response_text)
    elif response_text.startswith("That's not"):
        print(Fore.RED + response_text)
    elif response_text.startswith("You gave"):
        print(Fore.RED + response_text)
    else:
        raise ValueError(f"Unknown response text: {response_text}")
