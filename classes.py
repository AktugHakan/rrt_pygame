from __future__ import annotations
from math import sqrt
import sys
from constants import RRT_DISTANCE_MAX, RRT_DISTANCE_MIN

# Entity types
BASE = 0
GOAL = 1


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def calculate_distance(self, point: Point):
        return sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    def __iter__(self):
        return iter((self.x, self.y))

    def to_tuple(self) -> tuple[int, int]:
        return self.x, self.y


class Node:
    __slots__ = "prev", "next", "pos"

    def __init__(self, pos: Point, prev: Node | None = None) -> None:
        self.prev = prev
        self.next: list[Node] = []
        self.pos = pos


class CircleEntity:
    __slots__ = "pos", "radius", "entity_type"

    def __init__(self, x: int, y: int, radius: float, entity_type: int):
        self.pos: Point = Point(x, y)
        self.radius: float = radius
        self.entity_type: int = entity_type


class TreeMap:
    __slots__ = "tree"

    def __init__(self, initial_node_position: Point) -> None:
        self.tree: list[Node] = []
        init_node = Node(initial_node_position)
        self.tree.append(init_node)

    def find_nearest_node(self, new_point: Point) -> tuple[Node | None, float]:
        min_dist: float = sys.float_info.max
        nearest_node: Node | None = None
        for node in self.tree:
            distance = node.pos.calculate_distance(new_point)
            if distance < min_dist:
                min_dist = distance
                nearest_node = node

        return nearest_node, min_dist

    def __iter__(self):
        return iter(self.tree)

    def add_under(self, parent: Node, child: Node):
        self.tree.append(child)
        child.prev = parent
        parent.next.append(child)

    def get_root(self) -> Node:
        return self.tree[0]
