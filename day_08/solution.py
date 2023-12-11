# pyright: reportMissingTypeStubs=false

from __future__ import annotations

from dataclasses import dataclass, field
from math import lcm

from utils import SolutionAbstract


@dataclass(frozen=True, kw_only=True)
class _Node:
    name: str
    left_child_name: str
    right_child_name: str


@dataclass(frozen=True, kw_only=True)
class _Network:
    instructions: list[str]
    node_map: dict[str, _Node]
    instruction_count: int = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "instruction_count", len(self.instructions))

    def get_walker(
        self, *, start_node: _Node, step_count_offset: int = 0
    ) -> _NetworkWalker:
        return _NetworkWalker(
            network=self, start_node=start_node, step_count_offset=step_count_offset
        )


class _NetworkWalker:
    network: _Network
    current_node: _Node
    step_count: int
    step_count_offset: int

    def __init__(
        self,
        *,
        network: _Network,
        start_node: _Node,
        step_count_offset: int = 0,
    ) -> None:
        self.network = network
        self.current_node = start_node
        self.step_count = 0
        self.step_count_offset = step_count_offset

    def run_step(self) -> None:
        total_step_count = self.step_count + self.step_count_offset
        instruction_index = total_step_count % self.network.instruction_count
        step = self.network.instructions[instruction_index]
        match step:
            case "L":
                node_name = self.current_node.left_child_name
            case "R":
                node_name = self.current_node.right_child_name
            case _:
                raise ValueError(f"Invalid step {step}")
        self.current_node = self.network.node_map[node_name]
        self.step_count += 1


class Solution(SolutionAbstract, day=8):
    network: _Network

    def _process_data(self, raw_data: list[str]) -> None:
        """
        Process day 08 data.
        """
        data_iter = iter(raw_data)
        instructions = list(next(data_iter))
        next(data_iter)
        node_map = {}
        for row in data_iter:
            name, children_str = map(str.strip, row.split("="))
            left_child_name, right_child_name = map(
                str.strip, children_str.removeprefix("(").removesuffix(")").split(",")
            )
            node_map[name] = _Node(
                name=name,
                left_child_name=left_child_name,
                right_child_name=right_child_name,
            )
        self.network = _Network(instructions=instructions, node_map=node_map)

    def part_1(self, *, visualize: bool = False) -> int:
        """
        Day 08 part 1 solution.
        """
        walker = self.network.get_walker(start_node=self.network.node_map["AAA"])
        while walker.current_node.name != "ZZZ":
            walker.run_step()
        return walker.step_count

    def part_2(self, *, visualize: bool = False) -> int:
        """
        Day 08 part 2 solution.
        """
        full_loop_steps: list[int] = []
        for name, start_node in self.network.node_map.items():
            if not name.endswith("A"):
                continue
            # Find first Z
            walker = self.network.get_walker(start_node=start_node)
            while not walker.current_node.name.endswith("Z"):
                walker.run_step()
            # Find Z loop
            loop_walker = self.network.get_walker(
                start_node=walker.current_node, step_count_offset=walker.step_count
            )
            loop_walker.run_step()
            while not loop_walker.current_node.name.endswith("Z"):
                loop_walker.run_step()
            # This only applies because of specially constructed data
            assert walker.current_node.name == loop_walker.current_node.name
            assert walker.step_count == loop_walker.step_count
            full_loop_steps.append(walker.step_count)
        return lcm(*full_loop_steps)
