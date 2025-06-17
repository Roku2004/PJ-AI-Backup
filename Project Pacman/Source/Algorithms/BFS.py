from Extension.extension import find_nearest_food, DDX, Thief_check


def find_path_using_bfs(maze_map, food_positions, start_row, start_col, height, width):
    cells_visited = [[False for _ in range(width)] for _ in range(height)]
    path_tracker = [[[-1, -1] for _ in range(width)] for _ in range(height)]

    [target_row, target_col, food_index] = find_nearest_food(food_positions, start_row, start_col)

    if food_index == -1:
        return []

    queue = []
    found_path = False
    
    cells_visited[start_row][start_col] = True
    queue.append([start_row, start_col])
    
    while queue:
        [current_row, current_col] = queue.pop(0)

        if [current_row, current_col] == [target_row, target_col]:
            found_path = True
            break

        for [direction_row, direction_col] in DDX:
            next_row, next_col = current_row + direction_row, current_col + direction_col
            if Thief_check(maze_map, next_row, next_col, height, width) and not cells_visited[next_row][next_col]:
                cells_visited[next_row][next_col] = True
                queue.append([next_row, next_col])
                path_tracker[next_row][next_col] = [current_row, current_col]

    if not found_path:
        food_positions.pop(food_index)
        return find_path_using_bfs(maze_map, food_positions, start_row, start_col, height, width)

    final_path = [[target_row, target_col]]
    [backtrack_row, backtrack_col] = path_tracker[target_row][target_col]
    
    while backtrack_row != -1:
        final_path.insert(0, [backtrack_row, backtrack_col])
        [backtrack_row, backtrack_col] = path_tracker[backtrack_row][backtrack_col]

    return final_path