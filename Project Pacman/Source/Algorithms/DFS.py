from Extension.extension import DDX, Thief_check
from constants import FOOD


class DFSAgent:
    def __init__(self):
        self.maze_map = None
        self.food_positions = None
        self.height = 0
        self.width = 0
        self.visited = None
        self.path = None
        
    def initialize(self, maze_map, food_positions, height, width):
        
        self.maze_map = maze_map
        self.food_positions = food_positions
        self.height = height
        self.width = width
        self.visited = [[False for _ in range(width)] for _ in range(height)]
        self.path = []
        
    def is_food_position(self, row, col):
        
        return self.maze_map[row][col] == FOOD
        
    def get_valid_adjacent_positions(self, row, col):
        
        valid_positions = []
        
        for [direction_row, direction_col] in DDX:
            next_row, next_col = row + direction_row, col + direction_col
            if Thief_check(self.maze_map, next_row, next_col, self.height, self.width) and not self.visited[next_row][next_col]:
                valid_positions.append([next_row, next_col])
                
        return valid_positions
        
    def recursive_dfs(self, current_row, current_col):
        
        if self.visited[current_row][current_col]:
            return False
        
       
        self.visited[current_row][current_col] = True
        self.path.append([current_row, current_col])
        
       
        if self.is_food_position(current_row, current_col):
            return True
            
     
        for [next_row, next_col] in self.get_valid_adjacent_positions(current_row, current_col):
            if self.recursive_dfs(next_row, next_col):
                return True
                
       
        if self.path:
            self.path.pop()
            
        return False
        
    def find_path(self, start_row, start_col):
        
        success = self.recursive_dfs(start_row, start_col)
        
        if success:
           
            return self.path[1:] if len(self.path) > 1 else self.path
            
        return []


def find_path_using_dfs(maze_map, food_positions, start_row, start_col, height, width):
   
    agent = DFSAgent()
    agent.initialize(maze_map, food_positions, height, width)
    return agent.find_path(start_row, start_col)