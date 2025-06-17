from queue import PriorityQueue

from Extension.extension import Manhattan, DDX, Police_check


def move_police_using_astar(maze_map, start_row, start_col, end_row, end_col, height, width):
    cells_visited = [[False for _ in range(width)] for _ in range(height)]
    path_tracker = {}
    path_cost = {}
    path = []
    priority_queue = PriorityQueue()

    start_position = (start_row, start_col)
    target_position = (end_row, end_col)

    path_cost[start_position] = 0
    priority_queue.put((Manhattan(start_row, start_col, end_row, end_col), start_position))

    while not priority_queue.empty():
        current_position = priority_queue.get()[1]
        cells_visited[current_position[0]][current_position[1]] = True
        
        if current_position == target_position:
            path.append([current_position[0], current_position[1]])
            while current_position != start_position:
                current_position = path_tracker[current_position]
                path.append([current_position[0], current_position[1]])
            path.reverse()
            return path[1] if len(path) > 1 else [start_row, start_col]

        for [direction_row, direction_col] in DDX:
            next_row, next_col = current_position[0] + direction_row, current_position[1] + direction_col
            if Police_check(maze_map, next_row, next_col, height, width) and not cells_visited[next_row][next_col]:
                next_position = (next_row, next_col)
                path_cost[next_position] = path_cost[current_position] + 1
                priority_queue.put((path_cost[next_position] + Manhattan(next_row, next_col, end_row, end_col), next_position))
                path_tracker[next_position] = current_position

    return [start_row, start_col]