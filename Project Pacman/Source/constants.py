from enum import Enum


class Algorithm(Enum):
   
    LEVEL1 = "DFS"
    LEVEL2 = "BFS"
    LEVEL3 = "Local Search"
    LEVEL4 = "Minimax"


class Colors:
    
    BLACK = (28, 28, 28)
    WHITE = (248, 248, 248)
    BLUE = (66, 133, 244)
    GREEN = (52, 168, 83)
    RED = (234, 67, 53)
    PURPLE = (156, 39, 176)
    YELLOW = (251, 188, 4)
    ORANGE = (255, 138, 96)


class MapEntity:
    
    EMPTY = 0
    WALL = 1
    FOOD = 2
    POLICE = 3


class MapDimensions:
    
    SIZE_WALL = 30
    DEFINE_WIDTH = 6
    BLOCK_SIZE = SIZE_WALL // 2


class ScreenSettings:
    
    WIDTH = 1200
    HEIGHT = 600
    FPS = 300
    MARGIN = {
        "TOP": 0,
        "LEFT": 0
    }


class ImagePaths:
    
    POLICE = ["images/police1.png", "images/police2.png", 
              "images/police3.png", "images/police4.png"]
    THIEF = ["images/thief.png"]


LEVEL_TO_ALGORITHM = {
    "LEVEL1": Algorithm.LEVEL1.value,
    "LEVEL2": Algorithm.LEVEL2.value,
    "LEVEL3": Algorithm.LEVEL3.value,
    "LEVEL4": Algorithm.LEVEL4.value,
}


BLACK = Colors.BLACK
WHITE = Colors.WHITE
BLUE = Colors.BLUE
GREEN = Colors.GREEN
RED = Colors.RED
PURPLE = Colors.PURPLE
YELLOW = Colors.YELLOW
ORANGE = Colors.ORANGE


SIZE_WALL = MapDimensions.SIZE_WALL
DEFINE_WIDTH = MapDimensions.DEFINE_WIDTH
BLOCK_SIZE = MapDimensions.BLOCK_SIZE


EMPTY = MapEntity.EMPTY
WALL = MapEntity.WALL
FOOD = MapEntity.FOOD
POLICE = MapEntity.POLICE


WIDTH = ScreenSettings.WIDTH
HEIGHT = ScreenSettings.HEIGHT
FPS = ScreenSettings.FPS
MARGIN = ScreenSettings.MARGIN


IMAGE_POLICE = ImagePaths.POLICE
IMAGE_THIEF = ImagePaths.THIEF