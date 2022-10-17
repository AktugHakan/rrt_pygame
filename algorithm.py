from random import randint
from classes import CircleEntity, Point, TreeMap
from constants import (
    DRAW_RADIUS_GOAL,
    DRAW_RADIUS_NODE,
    DRAW_ACTIVE_SIZE,
    RRT_DISTANCE_MAX,
    RRT_DISTANCE_MIN,
)
from classes import TreeMap, CircleEntity, Node


def rrt_next_step(
    base: CircleEntity | None, goal: CircleEntity | None, tree_map: TreeMap | None
):
    while True and tree_map:
        x = randint(0, DRAW_ACTIVE_SIZE[0])
        y = randint(0, DRAW_ACTIVE_SIZE[1])
        new_position = Point(x, y)
        nearest_node, min_dist = tree_map.find_nearest_node(new_position)
        if (
            not nearest_node
            or min_dist > RRT_DISTANCE_MAX
            or min_dist < RRT_DISTANCE_MIN
        ):
            continue
        else:
            new_node = Node(new_position)
            tree_map.add_under(nearest_node, new_node)
            break


def check_found(tree_map: TreeMap, goal: CircleEntity | None) -> Node | None:
    if goal:
        nearest_node, min_dist = tree_map.find_nearest_node(goal.pos)
        if min_dist < DRAW_RADIUS_GOAL + DRAW_RADIUS_NODE:
            return nearest_node
        else:
            return None
    return None
