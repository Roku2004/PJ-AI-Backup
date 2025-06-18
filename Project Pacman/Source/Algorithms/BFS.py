from Extension.extension import find_nearest_food, DDX, Thief_check


class BFSAgent:
    def __init__(self):
        self.maze_map = None
        self.height = 0
        self.width = 0
        self.cells_visited = None
        self.path_tracker = None
        
    def initialize(self, maze_map, height, width):
      
        self.maze_map = maze_map
        self.height = height
        self.width = width
        self.cells_visited = [[False for _ in range(width)] for _ in range(height)]
        self.path_tracker = [[[-1, -1] for _ in range(width)] for _ in range(height)]
        
    def run_bfs(self, start_row, start_col, target_row, target_col):
       
        self.cells_visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.path_tracker = [[[-1, -1] for _ in range(self.width)] for _ in range(self.height)]
        
        queue = []
        found_path = False
        
        self.cells_visited[start_row][start_col] = True
        queue.append([start_row, start_col])
        
        while queue:
            [current_row, current_col] = queue.pop(0)
            
            if [current_row, current_col] == [target_row, target_col]:
                found_path = True
                break
                
            for [direction_row, direction_col] in DDX:
                next_row, next_col = current_row + direction_row, current_col + direction_col
                if Thief_check(self.maze_map, next_row, next_col, self.height, self.width) and not self.cells_visited[next_row][next_col]:
                    self.cells_visited[next_row][next_col] = True
                    queue.append([next_row, next_col])
                    self.path_tracker[next_row][next_col] = [current_row, current_col]
                    
        return found_path
        
    def reconstruct_path(self, target_row, target_col):
        
        if self.path_tracker[target_row][target_col] == [-1, -1]:
            return []
            
        final_path = [[target_row, target_col]]
        [backtrack_row, backtrack_col] = self.path_tracker[target_row][target_col]
        
        while backtrack_row != -1:
            final_path.insert(0, [backtrack_row, backtrack_col])
            [backtrack_row, backtrack_col] = self.path_tracker[backtrack_row][backtrack_col]
            
       
        return final_path[1:] if len(final_path) > 1 else final_path
        
    def find_path(self, food_positions, start_row, start_col):
       
        [target_row, target_col, food_index] = find_nearest_food(food_positions, start_row, start_col)
        
        if food_index == -1:
            return []
            
        found_path = self.run_bfs(start_row, start_col, target_row, target_col)
        
        if not found_path:
            
            food_positions.pop(food_index)
            return self.find_path(food_positions, start_row, start_col)
            
        return self.reconstruct_path(target_row, target_col)


def find_path_using_bfs(maze_map, food_positions, start_row, start_col, height, width):
    
    food_positions_copy = food_positions.copy()
    
    agent = BFSAgent()
    agent.initialize(maze_map, height, width)
    return agent.find_path(food_positions_copy, start_row, start_col)