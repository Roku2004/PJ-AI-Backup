from Extension.extension import DDX, Police_check
from constants import FOOD, POLICE, WALL

class LocalSearchAgent:
    def __init__(self):
        self.height = 0
        self.width = 0
        self.maze_map = None
        self.cost = None
        self.visit_count = None

    def setup(self, maze_map, height, width, visit_count):
       
        self.maze_map = maze_map
        self.height = height
        self.width = width
        self.visit_count = visit_count
        self.cost = [[0 for _ in range(width)] for _ in range(height)]

    def calculate_object_value(self, object_type, depth):
        if object_type == FOOD:
            if depth == 2:
                return 35
            if depth == 1:
                return 10
            if depth == 0:
                return 5
        elif object_type == POLICE:
            if depth == 2 or depth == 1:
                return float("-inf")
            if depth == 0:
                return -100
        return 0

    def update_heuristic(self, start_row, start_col, current_row, current_col, depth, visited, object_type):
       
        visited.append((current_row, current_col))

        if depth < 0:
            return
        if (start_row, start_col) == (current_row, current_col):
            return

        point = self.calculate_object_value(object_type, depth)
        self.cost[current_row][current_col] += point

        for [direction_row, direction_col] in DDX:
            next_row, next_col = current_row + direction_row, current_col + direction_col
            if Police_check(self.maze_map, next_row, next_col, self.height, self.width) and (next_row, next_col) not in visited:
                self.update_heuristic(start_row, start_col, next_row, next_col, depth - 1, visited.copy(), object_type)

    def calc_heuristic(self, start_row, start_col, current_row, current_col, depth, visited):
       

        if depth <= 0:
            return

        for [direction_row, direction_col] in DDX:
            next_row, next_col = current_row + direction_row, current_col + direction_col
            if Police_check(self.maze_map, next_row, next_col, self.height, self.width) and (next_row, next_col) not in visited:
                
               
                if self.maze_map[next_row][next_col] == FOOD:
                    self.update_heuristic(start_row, start_col, next_row, next_col, 2, [], FOOD)
                elif self.maze_map[next_row][next_col] == POLICE:
                    self.update_heuristic(start_row, start_col, next_row, next_col, 2, [], POLICE)

           
                self.calc_heuristic(start_row, start_col, next_row, next_col, depth - 1, visited.copy())
        
        
        self.cost[current_row][current_col] -= self.visit_count[current_row][current_col]

    def find_best_move(self, start_row, start_col):
        
        max_value = float("-inf")
        result = []
        
        for [direction_row, direction_col] in DDX:
            next_row, next_col = start_row + direction_row, start_col + direction_col
            
            if (0 <= next_row < self.height and 0 <= next_col < self.width and 
                self.maze_map[next_row][next_col] != WALL):
                adjusted_cost = self.cost[next_row][next_col] - self.visit_count[next_row][next_col]
                if adjusted_cost > max_value:
                    max_value = adjusted_cost
                    result = [next_row, next_col]
                    
        return result

    def find_path(self, start_row, start_col):
       
       
        self.cost = [[0 for _ in range(self.width)] for _ in range(self.height)]
        
       
        self.calc_heuristic(start_row, start_col, start_row, start_col, 3, [])
        
       
        return self.find_best_move(start_row, start_col)



def find_path_using_localsearch(maze_map, start_row, start_col, height, width, visit_count):
    agent = LocalSearchAgent()
    agent.setup(maze_map, height, width, visit_count)
    return agent.find_path(start_row, start_col)