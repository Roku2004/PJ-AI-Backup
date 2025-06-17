from constants import FOOD, EMPTY, WALL

# Directions: right, left, down, up
DDX = [[0, 1], [0, -1], [1, 0], [-1, 0]]


def Thief_check(maze_map, row: int, col: int, height: int, width: int) -> bool:
    """Check if the thief can move to this position"""
    return 0 < row < height and 0 < col < width and (maze_map[row][col] == FOOD or maze_map[row][col] == EMPTY)


def Police_check(maze_map, row: int, col: int, height: int, width: int) -> bool:
    """Check if the police can move to this position"""
    return 0 < row < height and 0 < col < width and maze_map[row][col] != WALL


def Manhattan(x1: int, y1: int, x2: int, y2: int) -> float:
    """Calculate Manhattan distance between two points"""
    return abs(x1 - x2) + abs(y1 - y2)


def find_nearest_food(food_positions: list[list[int]], start_row: int, start_col: int):
    """Find the nearest food position from the current position"""
    food_row, food_col, food_index = -1, -1, -1
    
    for idx in range(len(food_positions)):
        if food_row == -1:
            food_index = idx
            [food_row, food_col] = food_positions[idx]
        elif Manhattan(food_row, food_col, start_row, start_col) > Manhattan(food_positions[idx][0],
                                                                          food_positions[idx][1], start_row,
                                                                          start_col):
            food_index = idx
            [food_row, food_col] = food_positions[idx]

    return [food_row, food_col, food_index]