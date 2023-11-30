# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

import shutil
from argparse import ArgumentParser
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING

from colorama import Fore, init

from aoc_io import download_input, submit_output

if TYPE_CHECKING:
    from argparse import Namespace

    from .utils import SolutionAbstract

init(autoreset=True)

_PREPARATION_CMDS = ["e", "er", "prepare"]
_DOWNLOAD_CMDS = ["d", "dl", "download"]
_PRINT_CMDS = ["p", "pr", "print"]
_SUBMIT_CMDS = ["s", "sub", "submit"]
_METHOD_CMDS = ["m", "me", "method"]


def _main() -> None:
    """"""
    args = _get_args()

    # Prepare
    if args.command in _PREPARATION_CMDS:
        _prepare(day=args.day)
        return

    # Download input
    if args.command in _DOWNLOAD_CMDS:
        download_input(day=args.day)
        return

    # Get solution object
    solution_obj = _get_solution_obj(args.day)
    if args.command in _METHOD_CMDS:
        _run_method(solution_obj=solution_obj, day=args.day, method_name=args.method)
        return

    # Run and get solution
    if args.part is None:
        raise ValueError("No part number provided.")
    solution = _get_solution(solution_obj, args.part)
    if solution is None:
        print(f"{Fore.RED}No response got. This part may need manual processing.")
        return
    print(f"{Fore.GREEN}Got solution {solution!r}")
    if args.command in _SUBMIT_CMDS:
        submit_output(day=args.day, part=args.part, answer=solution)


def _get_args() -> Namespace:
    """"""
    parser = ArgumentParser(description="AoC 2022")
    subparsers = parser.add_subparsers(dest="command")

    # Preparations
    prep_parser = subparsers.add_parser("prepare", aliases=_PREPARATION_CMDS)
    prep_parser.add_argument("day", type=int, choices=range(1, 26))

    # Download
    dl_parser = subparsers.add_parser("download", aliases=_DOWNLOAD_CMDS)
    dl_parser.add_argument("day", type=int, choices=range(1, 26))

    # Print
    print_parser = subparsers.add_parser("print", aliases=_PRINT_CMDS)
    print_parser.add_argument("day", type=int, choices=range(1, 26))
    print_parser.add_argument("part", type=int, choices=(1, 2))

    # Submit
    submit_parser = subparsers.add_parser("submit", aliases=_SUBMIT_CMDS)
    submit_parser.add_argument("day", type=int, choices=range(1, 26))
    submit_parser.add_argument("part", type=int, choices=(1, 2), nargs="?")

    # Run method
    method_parser = subparsers.add_parser("method", aliases=_METHOD_CMDS)
    method_parser.add_argument("day", type=int, choices=range(1, 26))
    method_parser.add_argument("method")

    return parser.parse_args()


def _prepare(day: int) -> None:
    """"""
    parent_dir = Path(__file__).resolve().parent
    target_dir = parent_dir / f"day_{day:>02}"
    if not target_dir.exists():
        origin_dir = parent_dir / "day_xx"
        shutil.copytree(origin_dir, target_dir)
    for subpath in target_dir.iterdir():
        if subpath.suffix not in {".md", ".py"}:
            continue
        with subpath.open("r") as f:
            data = f.read()
        data = data.replace("xx", f"{day:>02}").replace("-1", str(day))
        with subpath.open("w") as f:
            f.write(data)
    print("Base URL: https://adventofcode.com/2022")
    print(f"Day URL: https://adventofcode.com/2022/{day}")
    download_input(day=day)


def _run_method(solution_obj: SolutionAbstract, day: int, method_name: str) -> None:
    """"""
    method = getattr(solution_obj, method_name)
    if not callable(method):
        raise ValueError(f"No method with name {method_name} on day {day}'s solution")
    result = method()
    print(f"{Fore.GREEN}{result}")


def _get_solution_obj(day: int) -> SolutionAbstract:
    """"""
    dir_name = f"day_{day:>02}"
    solution_module = import_module(f"{dir_name}.solution")
    SolutionClass: type[SolutionAbstract] = getattr(solution_module, "Solution")
    return SolutionClass()


def _get_solution(solution_obj: SolutionAbstract, part: int) -> str | int:
    """"""
    match part:
        case 1:
            return solution_obj.part_1()
        case 2:
            return solution_obj.part_2()
        case _:
            raise ValueError(f"Unknown part number {part}.")


if __name__ == "__main__":
    _main()
