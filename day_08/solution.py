# pyright: reportMissingTypeStubs=false

from __future__ import annotations

from dataclasses import dataclass
from math import lcm

from utils import SolutionAbstract


@dataclass(kw_only=True)
class _Node:
    name: str
    left_child_name: str
    right_child_name: str


class Solution(SolutionAbstract, day=8):
    instructions: list[str]
    node_map: dict[str, _Node]

    def _process_data(self, raw_data: list[str]) -> None:
        """
        Process day 08 data.
        """
        data_iter = iter(raw_data)
        self.instructions = list(next(data_iter))
        next(data_iter)
        self.node_map = {}
        for row in data_iter:
            name, children_str = map(str.strip, row.split("="))
            left_child_name, right_child_name = map(
                str.strip, children_str.removeprefix("(").removesuffix(")").split(",")
            )
            self.node_map[name] = _Node(
                name=name,
                left_child_name=left_child_name,
                right_child_name=right_child_name,
            )

    def part_1(self) -> int:
        """
        Day 08 part 1 solution.
        """
        step_count = 0
        node = self.node_map["AAA"]
        while node.name != "ZZZ":
            node = self._get_node_by_instruction(node=node, step_count=step_count)
            step_count += 1
        return step_count

    def part_2(self) -> int:
        """
        Day 08 part 2 solution.
        """
        full_loop_steps: list[int] = []
        for name, start_node in self.node_map.items():
            if not name.endswith("A"):
                continue
            step_count = 0
            node = start_node
            while not node.name.endswith("Z"):
                node = self._get_node_by_instruction(node=node, step_count=step_count)
                step_count += 1
            loop_size = 1
            node = self._get_node_by_instruction(node=node, step_count=step_count)
            while not node.name.endswith("Z"):
                node = self._get_node_by_instruction(
                    node=node, step_count=step_count + loop_size
                )
                loop_size += 1
            # This only applies because of specially constructed data
            assert loop_size == step_count
            full_loop_steps.append(step_count)
        return lcm(*full_loop_steps)

    def _get_node_by_instruction(self, *, node: _Node, step_count: int) -> _Node:
        step = self.instructions[step_count % len(self.instructions)]
        match step:
            case "L":
                node_name = node.left_child_name
            case "R":
                node_name = node.right_child_name
            case _:
                raise ValueError(f"Invalid step {step}")
        return self.node_map[node_name]
