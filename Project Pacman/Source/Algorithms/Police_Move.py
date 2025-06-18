from queue import PriorityQueue
from Extension.extension import Manhattan, DDX, Police_check


class AStarPoliceAgent:
    def __init__(self):
        self.maze_map = None
        self.height = 0
        self.width = 0
        self.cells_visited = None
        self.path_tracker = None
        self.path_cost = None
        
    def initialize(self, maze_map, height, width):
        """Initialize the agent with the maze map and dimensions."""
        self.maze_map = maze_map
        self.height = height
        self.width = width
        self.cells_visited = [[False for _ in range(width)] for _ in range(height)]
        self.path_tracker = {}
        self.path_cost = {}
        
    def heuristic(self, current_row, current_col, target_row, target_col):
        """Calculate heuristic cost using Manhattan distance."""
        return Manhattan(current_row, current_col, target_row, target_col)
        
    def get_valid_adjacent_positions(self, row, col):
        """Get all valid adjacent positions that police can move to."""
        valid_positions = []
        
        for [direction_row, direction_col] in DDX:
            next_row, next_col = row + direction_row, col + direction_col
            if Police_check(self.maze_map, next_row, next_col, self.height, self.width) and not self.cells_visited[next_row][next_col]:
                valid_positions.append((next_row, next_col))
                
        return valid_positions
        
    def reconstruct_path(self, start_position, target_position):
        """Reconstruct the path from target to start using path_tracker."""
        path = []
        current_position = target_position
        
        # Build the path backwards from target to start
        while current_position in self.path_tracker:
            path.append([current_position[0], current_position[1]])
            current_position = self.path_tracker[current_position]
            
        # Add the start position
        path.append([current_position[0], current_position[1]])
        
        # Reverse to get path from start to target
        path.reverse()
        
        # Return the next step after the start position
        return path[1] if len(path) > 1 else [start_position[0], start_position[1]]
        
    def run_astar(self, start_row, start_col, target_row, target_col):
        """Run A* algorithm to find best path from start to target."""
        # Reset data structures
        self.cells_visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.path_tracker = {}
        self.path_cost = {}
        
        start_position = (start_row, start_col)
        target_position = (target_row, target_col)
        
        # Initialize with starting position
        self.path_cost[start_position] = 0
        priority_queue = PriorityQueue()
        priority_queue.put((self.heuristic(start_row, start_col, target_row, target_col), start_position))
        
        while not priority_queue.empty():
            # Get position with lowest f-score (priority)
            current_position = priority_queue.get()[1]
            current_row, current_col = current_position
            
            # Mark as visited
            self.cells_visited[current_row][current_col] = True
            
            # Check if we've reached the target
            if current_position == target_position:
                return self.reconstruct_path(start_position, target_position)
                
            # Explore neighbors
            for next_position in self.get_valid_adjacent_positions(current_row, current_col):
                next_row, next_col = next_position
                
                # Calculate new cost to this neighbor
                new_cost = self.path_cost[current_position] + 1
                
                # If this is a new node or we found a better path
                if next_position not in self.path_cost or new_cost < self.path_cost[next_position]:
                    # Update the cost
                    self.path_cost[next_position] = new_cost
                    
                    # Calculate f-score (g + h) for priority queue
                    f_score = new_cost + self.heuristic(next_row, next_col, target_row, target_col)
                    
                    # Add to queue and update path
                    priority_queue.put((f_score, next_position))
                    self.path_tracker[next_position] = current_position
        
        # If no path is found, stay in place
        return [start_row, start_col]


def move_police_using_astar(maze_map, start_row, start_col, end_row, end_col, height, width):
    """Entry point function that maintains compatibility with the original code."""
    agent = AStarPoliceAgent()
    agent.initialize(maze_map, height, width)
    return agent.run_astar(start_row, start_col, end_row, end_col)