ALGORITHM: str = "MINIMAX"

LEVEL_TO_ALGORITHM = {
    "LEVEL1": "BFS",
    "LEVEL2": "BFS",
    "LEVEL3": "Local Search",
    "LEVEL4": "Minimax"
}

# DEFINE COLOR
BLACK = (28, 28, 28)
WHITE = (248, 248, 248)
BLUE = (66, 133, 244)
GREEN = (52, 168, 83)
RED = (234, 67, 53)
PURPLE = (156, 39, 176)
YELLOW = (251, 188, 4)
ORANGE = (255, 138, 96)

# DEFINE MAP
SIZE_WALL: int = 30
DEFINE_WIDTH: int = 6
BLOCK_SIZE: int = SIZE_WALL // 2

# Entity
EMPTY = 0
WALL = 1
FOOD = 2
MONSTER = 3

# Setup screen
WIDTH: int = 1200
HEIGHT: int = 600
FPS: int = 300

MARGIN = {
    "TOP": 0,
    "LEFT": 0
}


# IMAGE
IMAGE_GHOST = ["images/police1.png", "images/police2.png", "images/police3.png", "images/police4.png"]
IMAGE_PACMAN = ["images/thief.png"]
