# Algorithm mapping
LEVEL_TO_ALGORITHM = {
    "LEVEL1": "DFS",
    "LEVEL2": "BFS",
    "LEVEL3": "Local Search",
    "LEVEL4": "Minimax",
}

# Colors
BLACK = (28, 28, 28)
WHITE = (248, 248, 248)
BLUE = (66, 133, 244)
GREEN = (52, 168, 83)
RED = (234, 67, 53)
PURPLE = (156, 39, 176)
YELLOW = (251, 188, 4)
ORANGE = (255, 138, 96)

# Map dimensions
SIZE_WALL = 30
DEFINE_WIDTH = 6
BLOCK_SIZE = SIZE_WALL // 2

# Map entity types
EMPTY = 0
WALL = 1
FOOD = 2
POLICE = 3

# Screen setup
WIDTH = 1200
HEIGHT = 600
FPS = 300

# Screen margins
MARGIN = {
    "TOP": 0,
    "LEFT": 0
}

# Image paths
IMAGE_POLICE = ["images/police1.png", "images/police2.png", "images/police3.png", "images/police4.png"]
IMAGE_THIEF = ["images/thief.png"]