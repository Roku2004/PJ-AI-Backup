from Algorithms.BFS import find_path_using_bfs
from Algorithms.LocalSearch import find_path_using_localsearch
from Algorithms.Minimax import find_path_using_minimax
from Algorithms.DFS import find_path_using_dfs

class SearchAlgorithms:
    def __init__(self, maze_map, food_positions, start_row, start_col, height, width):
        self.maze_map = maze_map.copy()
        self.food_positions = food_positions.copy()
        self.start_row = start_row
        self.start_col = start_col
        self.height = height
        self.width = width

    def execute(self, ALGORITHMS, visited=None, depth=4, Score=0):
        if ALGORITHMS == "BFS":
            return find_path_using_bfs(self.maze_map, self.food_positions, self.start_row, self.start_col, self.height, self.width)
        if ALGORITHMS == "Local Search":
            return find_path_using_localsearch(self.maze_map, self.start_row, self.start_col, self.height, self.width, visited.copy())
        if ALGORITHMS == "Minimax":
            return find_path_using_minimax(self.maze_map, self.start_row, self.start_col, self.height, self.width, depth, Score)
        if ALGORITHMS == "DFS":
            return find_path_using_dfs(self.maze_map, self.food_positions, self.start_row, self.start_col, self.height, self.width)