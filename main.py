import pygame
import algorithm
from classes import CircleEntity, BASE, GOAL, Node, TreeMap, Point
from constants import *

DRAW_WINDOW_SIZE = (DRAW_ACTIVE_SIZE[0], DRAW_ACTIVE_SIZE[1] + DRAW_INFOPANEL_OFFSET_Y)
WINDOW = pygame.display.set_mode(DRAW_WINDOW_SIZE)


def main():
    pygame.init()
    pygame.display.set_caption("RRT Algorithm Demonstration")

    font = pygame.font.Font("freesansbold.ttf", DRAW_PUNTO_INFOPANEL_TEXT)
    text = font.render(
        "Space:Adım adım ilerle | Enter:Otomatik ilerle | Soltık:Başlangıç belirle | Sağ tık:Hedef belirle",
        True,
        DRAW_COLOR_INFOPANEL_TEXT,
    )
    text_outer_rect = pygame.Rect(
        0, DRAW_ACTIVE_SIZE[1], DRAW_ACTIVE_SIZE[0], DRAW_INFOPANEL_OFFSET_Y
    )
    text_inner_rect = pygame.Rect(
        10,
        DRAW_ACTIVE_SIZE[1] + 5,
        DRAW_ACTIVE_SIZE[0] - 10,
        DRAW_INFOPANEL_OFFSET_Y - 5,
    )
    text_info = (text, text_outer_rect, text_inner_rect)

    continue_loop = True
    run_until_found = False

    base = None
    goal = None
    tree_map: TreeMap | None = None
    found_node: Node | None = None
    # MAIN LOOP
    while continue_loop:
        # Event handling
        events = pygame.event.get()
        for event in events:
            match event.type:
                case pygame.QUIT:
                    continue_loop = False

                case pygame.MOUSEBUTTONDOWN:
                    entity = _create_new_entity()
                    if entity:
                        if entity.entity_type == BASE:
                            base = entity
                            tree_map = TreeMap(base.pos)
                        elif entity.entity_type == GOAL:
                            goal = entity

                case pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        algorithm.rrt_next_step(base, goal, tree_map)
                    elif (
                        (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN)
                        and base
                        and goal
                    ):
                        run_until_found = True

        if run_until_found:
            algorithm.rrt_next_step(base, goal, tree_map)

        if tree_map:
            found_node = algorithm.check_found(tree_map, goal)
            if found_node:
                run_until_found = False

        _draw(base, goal, tree_map, found_node, text_info)

    pygame.quit()


def _create_new_entity() -> CircleEntity | None:
    pressed_keys = pygame.mouse.get_pressed(3)
    left = False
    right = False
    if len(pressed_keys) == 3:
        left, _, right = pressed_keys
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    if left:
        return CircleEntity(mouse_pos_x, mouse_pos_y, DRAW_RADIUS_BASE, BASE)
    elif right:
        return CircleEntity(mouse_pos_x, mouse_pos_y, DRAW_RADIUS_GOAL, GOAL)
    else:
        return None


def _draw(
    base: CircleEntity | None,
    goal: CircleEntity | None,
    tree_map: TreeMap | None,
    found_node: Node | None = None,
    info_panel: tuple | None = None,
) -> None:

    WINDOW.fill(DRAW_COLOR_BACKGROUND)

    if base:
        pygame.draw.circle(WINDOW, DRAW_COLOR_BASE, base.pos.to_tuple(), base.radius)
    if goal:
        pygame.draw.circle(WINDOW, DRAW_COLOR_GOAL, goal.pos.to_tuple(), goal.radius)
    if tree_map:
        _draw_node_recursive(tree_map.get_root())
    if found_node:
        _draw_trace(found_node)
    if info_panel:
        pygame.draw.rect(WINDOW, DRAW_COLOR_INFOPANEL_BACKGROUND, info_panel[1])
        WINDOW.blit(info_panel[0], info_panel[2])

    pygame.display.update()


def _draw_node_recursive(node: Node):
    pygame.draw.circle(WINDOW, DRAW_COLOR_NODE, node.pos.to_tuple(), DRAW_RADIUS_NODE)
    for next_node in node.next:
        _draw_node_recursive(next_node)
        pygame.draw.line(
            WINDOW, DRAW_COLOR_LINE, node.pos.to_tuple(), next_node.pos.to_tuple()
        )


def _draw_trace(found_node: Node):
    current = found_node
    while current.prev:
        pygame.draw.circle(
            WINDOW, DRAW_COLOR_TRACE, current.pos.to_tuple(), DRAW_RADIUS_NODE
        )
        pygame.draw.line(
            WINDOW,
            DRAW_COLOR_TRACE,
            current.pos.to_tuple(),
            current.prev.pos.to_tuple(),
        )
        current = current.prev
    pygame.draw.circle(
        WINDOW, DRAW_COLOR_TRACE, current.pos.to_tuple(), DRAW_RADIUS_NODE
    )


main()
