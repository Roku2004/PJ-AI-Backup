from Extension.extension import Manhattan, DDX, Police_check, Thief_check
from constants import FOOD, POLICE, EMPTY

food_positions_cache = []


def evaluate_state(maze_map, thief_row, thief_col, height, width, score):
    police_positions = []
    food_distances = []
    
    for row in range(height): 
        for col in range(width):
            if maze_map[row][col] == FOOD:
                food_distances.append(Manhattan(row, col, thief_row, thief_col))
            if maze_map[row][col] == POLICE:
                police_positions.append([row, col])
            if maze_map[row][col] == EMPTY:
                score += 5

    # Constants
    INF = 1000000
    FOOD_WEIGHT = 200
    POLICE_WEIGHT = -250

    # Calculate score
    final_score = score
    
    if food_distances:
        min_distance = min(food_distances) if min(food_distances) != 0 else 1
        final_score += FOOD_WEIGHT / min_distance
    else:
        final_score += FOOD_WEIGHT

    for [police_row, police_col] in police_positions:
        distance = Manhattan(thief_row, thief_col, police_row, police_col)
        if distance > 0:
            final_score += POLICE_WEIGHT / distance
        else:
            return -INF

    return final_score


def find_path_using_minimax(maze_map, thief_row, thief_col, height, width, depth, score):
    def is_terminal(current_map, current_thief_row, current_thief_col, map_height, map_width, current_depth):
        if current_map[current_thief_row][current_thief_col] == POLICE or current_depth == 0:
            return True

        for row in range(map_height):
            for col in range(map_width):
                if current_map[row][col] == FOOD:
                    return False

        return True

    def min_value(current_map, current_thief_row, current_thief_col, map_height, map_width, current_depth, current_score):
        if is_terminal(current_map, current_thief_row, current_thief_col, map_height, map_width, current_depth):
            return evaluate_state(current_map, current_thief_row, current_thief_col, map_height, map_width, current_score)

        value = float("inf")
        
        for row in range(map_height):
            for col in range(map_width):
                if current_map[row][col] == POLICE:
                    for [direction_row, direction_col] in DDX:
                        next_row, next_col = direction_row + row, direction_col + col
                        if Police_check(current_map, next_row, next_col, map_height, map_width):
                            state = current_map[next_row][next_col]
                            current_map[next_row][next_col] = POLICE
                            current_map[row][col] = EMPTY
                            value = min(value, max_value(current_map, current_thief_row, current_thief_col, map_height, map_width, current_depth - 1, current_score))
                            current_map[next_row][next_col] = state
                            current_map[row][col] = POLICE
        
        return value

    def max_value(current_map, current_thief_row, current_thief_col, map_height, map_width, current_depth, current_score):
        if is_terminal(current_map, current_thief_row, current_thief_col, map_height, map_width, current_depth):
            return evaluate_state(current_map, current_thief_row, current_thief_col, map_height, map_width, current_score)

        value = float("-inf")
        
        for [direction_row, direction_col] in DDX:
            next_row, next_col = current_thief_row + direction_row, current_thief_col + direction_col
            
            if Thief_check(current_map, next_row, next_col, map_height, map_width):
                state = current_map[next_row][next_col]
                current_map[next_row][next_col] = EMPTY
                local_score = current_score
                
                if state == FOOD:
                    local_score += 40
                    food_positions_cache.pop(food_positions_cache.index((next_row, next_col)))
                else:
                    local_score -= 10
                    
                value = max(value, min_value(current_map, next_row, next_col, map_height, map_width, current_depth - 1, local_score))
                
                current_map[next_row][next_col] = state
                
                if state == FOOD:
                    food_positions_cache.append((next_row, next_col))
                    
        return value

    # Main function
    possible_moves = []
    global food_positions_cache
    food_positions_cache = []
    
    for row in range(height):
        for col in range(width):
            if maze_map[row][col] == FOOD:
                food_positions_cache.append((row, col))

    for [direction_row, direction_col] in DDX:
        next_row, next_col = thief_row + direction_row, thief_col + direction_col
        
        if Thief_check(maze_map, next_row, next_col, height, width):
            current_state = maze_map[next_row][next_col]
            maze_map[next_row][next_col] = EMPTY
            local_score = score
            
            if current_state == FOOD:
                local_score += 40
                food_positions_cache.pop(food_positions_cache.index((next_row, next_col)))
            else:
                local_score -= 10
                
            possible_moves.append(([next_row, next_col], min_value(maze_map, next_row, next_col, height, width, depth, local_score)))
            
            maze_map[next_row][next_col] = current_state
            
            if current_state == FOOD:
                food_positions_cache.append((next_row, next_col))

    possible_moves.sort(key=lambda k: k[1])
    
    if possible_moves:
        return possible_moves[-1][0]  # Return position with highest evaluation
        
    return []