import sys
import pygame
import random

from Algorithms.Police_Move import move_police_using_astar
from Algorithms.SearchAlgorithms import SearchAlgorithms
from Object.Food import Food
from Object.Player import Player
from Object.Wall import Wall
from Extension.extension import DDX, Police_check, Thief_check
from constants import *
from Object.Menu import Menu, Button

# Game state variables
height = width = score = thief_animation_state = 0
maze_map = []
wall_objects = []
road_objects = []
food_objects = []
police_objects = []
food_positions = []
police_positions = []
visit_counter = []
thief_player = None
current_level = 1
map_file_path = ""

# Initialize Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Thief')
clock = pygame.time.Clock()

pygame.font.init()
game_font = pygame.font.SysFont('Comic Sans MS', 30)
large_font = pygame.font.SysFont('Comic Sans MS', 100)


def load_map_from_file(map_name: str):
    """Load map data from file"""
    f = open(map_name, "r")
    x = f.readline().split()
    global height, width, maze_map
    maze_map = []
    height, width = int(x[0]), int(x[1])
    for _ in range(height):
        line = f.readline().split()
        map_row = []
        for j in range(width):
            map_row.append(int(line[j]))
        maze_map.append(map_row)

    global thief_player
    x = f.readline().split()

    MARGIN["TOP"] = max(0, (HEIGHT - height * SIZE_WALL) // 2)
    MARGIN["LEFT"] = max(0, (WIDTH - width * SIZE_WALL) // 2)
    thief_player = Player(int(x[0]), int(x[1]), IMAGE_THIEF[0])

    f.close()


def process_map_object(map_array, row, col):
    """Process map objects at the given position"""
    if map_array[row][col] == WALL:
        wall_objects.append(Wall(row, col, BLUE))

    if map_array[row][col] == FOOD:
        food_objects.append(Food(row, col, BLOCK_SIZE, BLOCK_SIZE, YELLOW))
        food_positions.append([row, col])

    if map_array[row][col] == POLICE:
        police_objects.append(Player(row, col, IMAGE_POLICE[len(police_objects) % len(IMAGE_POLICE)]))
        police_positions.append([row, col])


def initialize_game_data():
    """Initialize all game data"""
    global height, width, maze_map, food_positions, food_objects, road_objects
    global wall_objects, police_objects, visit_counter, score, thief_animation_state, police_positions
    
    height = width = score = thief_animation_state = 0
    maze_map = []
    wall_objects = []
    road_objects = []
    food_objects = []
    police_objects = []
    food_positions = []
    police_positions = []

    load_map_from_file(map_name=map_file_path)
    visit_counter = [[0 for _ in range(width)] for _ in range(height)]

    for row in range(height):
        for col in range(width):
            process_map_object(maze_map, row, col)


def draw_game_objects(surface):
    """Draw all game objects on the screen"""
    for wall in wall_objects:
        wall.draw(surface)
    for road in road_objects:
        road.draw(surface)
    for food in food_objects:
        food.draw(surface)
    for police in police_objects:
        police.draw(surface)

    thief_player.draw(surface)

    text_surface = game_font.render(f'Score: {score}', False, RED)
    surface.blit(text_surface, (0, 0))


def generate_police_movements(police_list, movement_type=0):
    """Generate new positions for police objects based on the movement type"""
    new_police_positions = []
    
    # Random movement
    if movement_type == 1:
        for idx in range(len(police_list)):
            [row, col] = police_list[idx].getRC()

            direction = random.randint(0, 3)
            new_row, new_col = row + DDX[direction][0], col + DDX[direction][1]
            while not Police_check(maze_map, new_row, new_col, height, width):
                direction = random.randint(0, 3)
                new_row, new_col = row + DDX[direction][0], col + DDX[direction][1]

            new_police_positions.append([new_row, new_col])

    # A* pathfinding to chase thief
    elif movement_type == 2:
        for idx in range(len(police_list)):
            [police_row, police_col] = police_list[idx].getRC()
            [thief_row, thief_col] = thief_player.getRC()
            new_police_positions.append(move_police_using_astar(maze_map, police_row, police_col, thief_row, thief_col, height, width))

    return new_police_positions


def check_collision_with_police(police_list, thief_row=-1, thief_col=-1):
    """Check if thief collides with any police"""
    thief_position = [thief_row, thief_col]
    if thief_row == -1:
        thief_position = thief_player.getRC()
        
    for police in police_list:
        police_position = police.getRC()
        if thief_position == police_position:
            return True

    return False


def update_thief_direction(new_row, new_col):
    """Update thief direction based on new position"""
    global thief_player, thief_animation_state
    [current_row, current_col] = thief_player.getRC()
    thief_animation_state = (thief_animation_state + 1) % len(IMAGE_THIEF)

    if new_row > current_row:
        thief_player.change_state(-90, IMAGE_THIEF[thief_animation_state])
    elif new_row < current_row:
        thief_player.change_state(90, IMAGE_THIEF[thief_animation_state])
    elif new_col > current_col:
        thief_player.change_state(0, IMAGE_THIEF[thief_animation_state])
    elif new_col < current_col:
        thief_player.change_state(180, IMAGE_THIEF[thief_animation_state])


def get_random_valid_move(map_array, row, col, height_limit, width_limit):
    """Find a random valid move for thief when algorithms fail"""
    for [direction_row, direction_col] in DDX:
        new_row, new_col = direction_row + row, direction_col + col
        if Thief_check(map_array, new_row, new_col, height_limit, width_limit):
            return [new_row, new_col]
    return []


def start_game():
    """Start and run the game"""
    global maze_map, visit_counter, score
    police_new_positions = []
    result = []
    new_thief_position = []
    initialize_game_data()
    thief_can_move = True

    game_exit = False
    is_moving = False
    movement_timer = 0

    game_status = 0
    delay = 100

    # Main game loop
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_menu()
                return

        if delay > 0:
            delay -= 1
            
        # Handle movement step by step
        if delay <= 0:
            if is_moving:  # Characters are moving
                movement_timer += 1 

                # Police movement
                if police_new_positions:
                    for idx in range(len(police_objects)):
                        [old_police_row, old_police_col] = police_objects[idx].getRC()
                        [new_police_row, new_police_col] = police_new_positions[idx]

                        if old_police_row < new_police_row:
                            police_objects[idx].move(1, 0)  # Move down
                        elif old_police_row > new_police_row:
                            police_objects[idx].move(-1, 0)  # Move up
                        elif old_police_col < new_police_col:
                            police_objects[idx].move(0, 1)  # Move right
                        elif old_police_col > new_police_col:
                            police_objects[idx].move(0, -1)  # Move left

                        if movement_timer >= SIZE_WALL: 
                            police_objects[idx].setRC(new_police_row, new_police_col)

                            maze_map[old_police_row][old_police_col] = EMPTY
                            maze_map[new_police_row][new_police_col] = POLICE

                            # Check if police moved over food
                            for index in range(len(food_objects)):
                                [food_row, food_col] = food_objects[index].getRC()
                                if food_row == old_police_row and food_col == old_police_col:
                                    maze_map[food_row][food_col] = FOOD

                # Thief movement
                if new_thief_position:
                    [old_thief_row, old_thief_col] = thief_player.getRC()
                    [new_thief_row, new_thief_col] = new_thief_position

                    if old_thief_row < new_thief_row:
                        thief_player.move(1, 0)  # Move down
                    elif old_thief_row > new_thief_row:
                        thief_player.move(-1, 0)  # Move up
                    elif old_thief_col < new_thief_col:
                        thief_player.move(0, 1)  # Move right
                    elif old_thief_col > new_thief_col:
                        thief_player.move(0, -1)  # Move left

                    if movement_timer >= SIZE_WALL or thief_player.touch_New_RC(new_thief_row, new_thief_col):
                        is_moving = False
                        thief_player.setRC(new_thief_row, new_thief_col)
                        score -= 1

                        # Check if thief collected food
                        for idx in range(len(food_objects)):
                            [food_row, food_col] = food_objects[idx].getRC()
                            if food_row == new_thief_row and food_col == new_thief_col:
                                maze_map[food_row][food_col] = EMPTY
                                food_objects.pop(idx)
                                food_positions.pop(idx)
                                score += 20
                                break
                        new_thief_position = []

                # Check for collisions and end conditions
                if check_collision_with_police(police_objects):
                    thief_can_move = False
                    game_exit = True
                    game_status = -1  # Thief loses

                if not food_positions:
                    game_status = 1  # Thief wins
                    game_exit = True

                if movement_timer >= SIZE_WALL:
                    is_moving = False
            else:
                # Generate police movements based on level
                if current_level == 3:
                    police_new_positions = generate_police_movements(police_objects, movement_type=1)
                elif current_level == 4:
                    police_new_positions = generate_police_movements(police_objects, movement_type=2)
                else:
                    police_new_positions = generate_police_movements(police_objects, movement_type=0)

                is_moving = True
                movement_timer = 0

                if not thief_can_move:
                    continue

                [thief_row, thief_col] = thief_player.getRC()

                # Algorithm selection based on level
                search = SearchAlgorithms(maze_map, food_positions, thief_row, thief_col, height, width)
                
                if current_level == 1:
                    if not result:
                        result = search.execute(ALGORITHMS=LEVEL_TO_ALGORITHM["LEVEL1"])
                        if result:
                            result.pop(0)
                            new_thief_position = result[0] if result else []

                    elif len(result) > 1:
                        result.pop(0)
                        new_thief_position = result[0]
                elif current_level == 2:
                    if not result:
                        result = search.execute(ALGORITHMS=LEVEL_TO_ALGORITHM["LEVEL2"])
                        if result:
                            result.pop(0)
                            new_thief_position = result[0] if result else []

                    elif len(result) > 1:
                        result.pop(0)
                        new_thief_position = result[0]
                elif current_level == 3 and food_positions:
                    new_thief_position = search.execute(ALGORITHMS=LEVEL_TO_ALGORITHM["LEVEL3"], visited=visit_counter)
                    visit_counter[thief_row][thief_col] += 1

                elif current_level == 4 and food_positions:
                    new_thief_position = search.execute(ALGORITHMS=LEVEL_TO_ALGORITHM["LEVEL4"], depth=4, Score=score)

                # Fallback for when no path is found
                if food_positions and (not new_thief_position or [thief_row, thief_col] == new_thief_position):
                    new_thief_position = get_random_valid_move(maze_map, thief_row, thief_col, height, width)
                    
                if new_thief_position:
                    update_thief_direction(new_thief_position[0], new_thief_position[1])
                    if check_collision_with_police(police_objects, new_thief_position[0], new_thief_position[1]):
                        thief_can_move = False
                        game_exit = True
                        game_status = -1

        # Render game
        screen.fill(BLACK)
        draw_game_objects(screen)
        pygame.display.flip()
        clock.tick(FPS)

    handle_game_end(game_status)


game_end_done = False


def handle_game_end(status):
    """Handle end game screen"""
    global game_end_done
    game_end_done = False
    lose_bg = pygame.image.load("images/gameover.png")
    lose_bg = pygame.transform.scale(lose_bg, (WIDTH, HEIGHT))
    win_bg = pygame.image.load("images/win1.png")
    win_bg = pygame.transform.scale(win_bg, (WIDTH, HEIGHT))

    def click_continue():
        global game_end_done
        game_end_done = True

    def click_quit():
        pygame.quit()
        sys.exit(0)

    btn_continue = Button(WIDTH // 2 - 300, HEIGHT // 2 - 50, 200, 100, screen, "CONTINUE", click_continue)
    btn_quit = Button(WIDTH // 2 + 50, HEIGHT // 2 - 50, 200, 100, screen, "QUIT", click_quit)

    delay = 100
    while not game_end_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        if delay > 0:
            delay -= 1
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if status == -1:
            screen.blit(lose_bg, (0, 0))
        else:
            screen.blit(win_bg, (0, 0))
            score_text = large_font.render(f'Your Score: {score}', False, RED)
            screen.blit(score_text, (WIDTH // 4 - 65, 10))

        btn_quit.process()
        btn_continue.process()

        pygame.display.flip()
        clock.tick(FPS)

    show_menu()


def show_menu():
    """Show game menu"""
    menu = Menu(screen)
    global current_level, map_file_path
    [current_level, map_file_path] = menu.run()
    start_game()


if __name__ == '__main__':
    show_menu()
    pygame.quit()