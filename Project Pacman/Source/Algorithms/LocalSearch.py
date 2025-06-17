from Extension.extension import DDX, Police_check
from constants import FOOD, POLICE, WALL


def update_heuristic(maze_map, start_row, start_col, current_row, current_col, height, width, depth, visited, object_type, cost):
    visited.append((current_row, current_col))

    if depth < 0:
        return
    if (start_row, start_col) == (current_row, current_col):
        return

    point = 0
    if object_type == FOOD:
        if depth == 2:
            point = 35
        if depth == 1:
            point = 10
        if depth == 0:
            point = 5
    elif object_type == POLICE:
        if depth == 2:
            point = float("-inf")
        if depth == 1:
            point = float("-inf")
        if depth == 0:
            point = -100

    cost[current_row][current_col] += point

    for [direction_row, direction_col] in DDX:
        next_row, next_col = current_row + direction_row, current_col + direction_col
        if Police_check(maze_map, next_row, next_col, height, width) and (next_row, next_col) not in visited:
            update_heuristic(maze_map, start_row, start_col, next_row, next_col, height, width, depth - 1, visited.copy(), object_type, cost)


def calc_heuristic(maze_map, start_row, start_col, current_row, current_col, height, width, depth, visited, cost, visit_count):
    visited.append((current_row, current_col))

    if depth <= 0:
        return

    for [direction_row, direction_col] in DDX:
        next_row, next_col = current_row + direction_row, current_col + direction_col
        if Police_check(maze_map, next_row, next_col, height, width) and (next_row, next_col) not in visited:

            sub_visited = []
            if maze_map[next_row][next_col] == FOOD:
                update_heuristic(maze_map, start_row, start_col, next_row, next_col, height, width, 2, sub_visited, FOOD, cost)
            elif maze_map[next_row][next_col] == POLICE:
                update_heuristic(maze_map, start_row, start_col, next_row, next_col, height, width, 2, sub_visited, POLICE, cost)

            calc_heuristic(maze_map, start_row, start_col, next_row, next_col, height, width, depth - 1, visited.copy(), cost, visit_count)

    cost[current_row][current_col] -= visit_count[current_row][current_col]


def find_path_using_localsearch(maze_map, start_row, start_col, height, width, visit_count):
    visited = []
    cost = [[0 for _ in range(width)] for _ in range(height)]

    calc_heuristic(maze_map, start_row, start_col, start_row, start_col, height, width, 3, visited, cost, visit_count)

    max_value = float("-inf")
    result = []
    
    for [direction_row, direction_col] in DDX:
        next_row, next_col = start_row + direction_row, start_col + direction_col
        if cost[next_row][next_col] - visit_count[next_row][next_col] > max_value and maze_map[next_row][next_col] != WALL:
            max_value = cost[next_row][next_col] - visit_count[next_row][next_col]
            result = [next_row, next_col]

    return result