from Extension.extension import DDX, Thief_check
from constants import FOOD


def recursive_dfs(maze_map, food_positions, current_row, current_col, height, width, visited, path):
    if visited[current_row][current_col]:
        return 0
    
    visited[current_row][current_col] = True
    path.append([current_row, current_col])
    
    if maze_map[current_row][current_col] == FOOD:
        return 1

    for [direction_row, direction_col] in DDX:
        next_row, next_col = current_row + direction_row, current_col + direction_col
        if Thief_check(maze_map, next_row, next_col, height, width) and not visited[next_row][next_col]:
            result = recursive_dfs(maze_map, food_positions, next_row, next_col, height, width, visited, path)
            if result == 1:
                return 1
                
            if path:
                path.pop()

    return 0


def find_path_using_dfs(maze_map, food_positions, start_row, start_col, height, width):
    visited = [[False for _ in range(width)] for _ in range(height)]
    path = []

    result = recursive_dfs(maze_map, food_positions, start_row, start_col, height, width, visited, path)

    if result == 1:
        return path

    return []