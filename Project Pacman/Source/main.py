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


class GameState:
    def __init__(self):
        self.height = 0
        self.width = 0
        self.score = 0
        self.thief_animation_state = 0
        self.maze_map = []
        self.wall_objects = []
        self.road_objects = []
        self.food_objects = []
        self.police_objects = []
        self.food_positions = []
        self.police_positions = []
        self.visit_counter = []
        self.thief_player = None
        self.current_level = 1
        self.map_file_path = ""
        self.game_end_done = False
        
    def reset(self):
        self.height = 0
        self.width = 0
        self.score = 0
        self.thief_animation_state = 0
        self.maze_map = []
        self.wall_objects = []
        self.road_objects = []
        self.food_objects = []
        self.police_objects = []
        self.food_positions = []
        self.police_positions = []


class GameManager:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        self.state = GameState()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Thief')
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.large_font = pygame.font.SysFont('Comic Sans MS', 100)
        
    def load_map_from_file(self, map_name):
        f = open(map_name, "r")
        x = f.readline().split()
        
        self.state.maze_map = []
        self.state.height, self.state.width = int(x[0]), int(x[1])
        
        for _ in range(self.state.height):
            line = f.readline().split()
            map_row = []
            for j in range(self.state.width):
                map_row.append(int(line[j]))
            self.state.maze_map.append(map_row)

        x = f.readline().split()
        MARGIN["TOP"] = max(0, (HEIGHT - self.state.height * SIZE_WALL) // 2)
        MARGIN["LEFT"] = max(0, (WIDTH - self.state.width * SIZE_WALL) // 2)
        self.state.thief_player = Player(int(x[0]), int(x[1]), IMAGE_THIEF[0])
        f.close()
        
    def process_map_object(self, row, col):
        if self.state.maze_map[row][col] == WALL:
            self.state.wall_objects.append(Wall(row, col, BLUE))

        if self.state.maze_map[row][col] == FOOD:
            self.state.food_objects.append(Food(row, col, BLOCK_SIZE, BLOCK_SIZE, YELLOW))
            self.state.food_positions.append([row, col])

        if self.state.maze_map[row][col] == POLICE:
            police_img = IMAGE_POLICE[len(self.state.police_objects) % len(IMAGE_POLICE)]
            self.state.police_objects.append(Player(row, col, police_img))
            self.state.police_positions.append([row, col])
            
    def initialize_game_data(self):
        self.state.reset()
        
        self.load_map_from_file(map_name=self.state.map_file_path)
        self.state.visit_counter = [[0 for _ in range(self.state.width)] for _ in range(self.state.height)]

        for row in range(self.state.height):
            for col in range(self.state.width):
                self.process_map_object(row, col)
                
    def draw_game_objects(self):
        for wall in self.state.wall_objects:
            wall.draw(self.screen)
        for road in self.state.road_objects:
            road.draw(self.screen)
        for food in self.state.food_objects:
            food.draw(self.screen)
        for police in self.state.police_objects:
            police.draw(self.screen)

        self.state.thief_player.draw(self.screen)

        text_surface = self.game_font.render(f'Score: {self.state.score}', False, RED)
        self.screen.blit(text_surface, (0, 0))
        
    def generate_police_movements(self, movement_type=0):
        new_police_positions = []
        
        if movement_type == 1:
            for idx, police in enumerate(self.state.police_objects):
                [row, col] = police.getRC()

                direction = random.randint(0, 3)
                new_row, new_col = row + DDX[direction][0], col + DDX[direction][1]
                while not Police_check(self.state.maze_map, new_row, new_col, self.state.height, self.state.width):
                    direction = random.randint(0, 3)
                    new_row, new_col = row + DDX[direction][0], col + DDX[direction][1]

                new_police_positions.append([new_row, new_col])

        elif movement_type == 2:
            for police in self.state.police_objects:
                [police_row, police_col] = police.getRC()
                [thief_row, thief_col] = self.state.thief_player.getRC()
                new_pos = move_police_using_astar(
                    self.state.maze_map, police_row, police_col, 
                    thief_row, thief_col, self.state.height, self.state.width
                )
                new_police_positions.append(new_pos)

        return new_police_positions
        
    def check_collision_with_police(self, thief_row=-1, thief_col=-1):
        thief_position = [thief_row, thief_col]
        if thief_row == -1:
            thief_position = self.state.thief_player.getRC()
            
        for police in self.state.police_objects:
            police_position = police.getRC()
            if thief_position == police_position:
                return True

        return False
        
    def update_thief_direction(self, new_row, new_col):
        [current_row, current_col] = self.state.thief_player.getRC()
        self.state.thief_animation_state = (self.state.thief_animation_state + 1) % len(IMAGE_THIEF)

        if new_row > current_row:
            self.state.thief_player.change_state(-90, IMAGE_THIEF[self.state.thief_animation_state])
        elif new_row < current_row:
            self.state.thief_player.change_state(90, IMAGE_THIEF[self.state.thief_animation_state])
        elif new_col > current_col:
            self.state.thief_player.change_state(0, IMAGE_THIEF[self.state.thief_animation_state])
        elif new_col < current_col:
            self.state.thief_player.change_state(180, IMAGE_THIEF[self.state.thief_animation_state])
            
    def get_random_valid_move(self, row, col):
        for [direction_row, direction_col] in DDX:
            new_row, new_col = direction_row + row, direction_col + col
            if Thief_check(self.state.maze_map, new_row, new_col, self.state.height, self.state.width):
                return [new_row, new_col]
        return []
        
    def process_police_movement(self, police_new_positions, movement_timer):
        for idx in range(len(self.state.police_objects)):
            [old_police_row, old_police_col] = self.state.police_objects[idx].getRC()
            [new_police_row, new_police_col] = police_new_positions[idx]

            if old_police_row < new_police_row:
                self.state.police_objects[idx].move(1, 0)
            elif old_police_row > new_police_row:
                self.state.police_objects[idx].move(-1, 0)
            elif old_police_col < new_police_col:
                self.state.police_objects[idx].move(0, 1)
            elif old_police_col > new_police_col:
                self.state.police_objects[idx].move(0, -1)

            if movement_timer >= SIZE_WALL: 
                self.state.police_objects[idx].setRC(new_police_row, new_police_col)

                self.state.maze_map[old_police_row][old_police_col] = EMPTY
                self.state.maze_map[new_police_row][new_police_col] = POLICE

                for index in range(len(self.state.food_objects)):
                    [food_row, food_col] = self.state.food_objects[index].getRC()
                    if food_row == old_police_row and food_col == old_police_col:
                        self.state.maze_map[food_row][food_col] = FOOD
                        break
                        
    def process_thief_movement(self, new_thief_position, movement_timer):
        [old_thief_row, old_thief_col] = self.state.thief_player.getRC()
        [new_thief_row, new_thief_col] = new_thief_position

        if old_thief_row < new_thief_row:
            self.state.thief_player.move(1, 0)
        elif old_thief_row > new_thief_row:
            self.state.thief_player.move(-1, 0)
        elif old_thief_col < new_thief_col:
            self.state.thief_player.move(0, 1)
        elif old_thief_col > new_thief_col:
            self.state.thief_player.move(0, -1)

        movement_complete = (movement_timer >= SIZE_WALL or 
                            self.state.thief_player.touch_New_RC(new_thief_row, new_thief_col))
        
        if movement_complete:
            self.state.thief_player.setRC(new_thief_row, new_thief_col)
            self.state.score -= 1

            for idx in range(len(self.state.food_objects)):
                [food_row, food_col] = self.state.food_objects[idx].getRC()
                if food_row == new_thief_row and food_col == new_thief_col:
                    self.state.maze_map[food_row][food_col] = EMPTY
                    self.state.food_objects.pop(idx)
                    self.state.food_positions.pop(idx)
                    self.state.score += 20
                    break
                    
            return True
        return False
        
    def calculate_thief_move(self, thief_row, thief_col, result):
        search = SearchAlgorithms(self.state.maze_map, self.state.food_positions, 
                                 thief_row, thief_col, self.state.height, self.state.width)
        
        new_thief_position = []
        
        if self.state.current_level == 1:
            if not result:
                result = search.execute(ALGORITHMS=LEVEL_TO_ALGORITHM["LEVEL1"])
                if result:
                    result.pop(0)
                    new_thief_position = result[0] if result else []
            elif len(result) > 1:
                result.pop(0)
                new_thief_position = result[0]
                
        elif self.state.current_level == 2:
            if not result:
                result = search.execute(ALGORITHMS=LEVEL_TO_ALGORITHM["LEVEL2"])
                if result:
                    result.pop(0)
                    new_thief_position = result[0] if result else []
            elif len(result) > 1:
                result.pop(0)
                new_thief_position = result[0]
                
        elif self.state.current_level == 3 and self.state.food_positions:
            new_thief_position = search.execute(ALGORITHMS=LEVEL_TO_ALGORITHM["LEVEL3"], 
                                              visited=self.state.visit_counter)
            self.state.visit_counter[thief_row][thief_col] += 1

        elif self.state.current_level == 4 and self.state.food_positions:
            new_thief_position = search.execute(ALGORITHMS=LEVEL_TO_ALGORITHM["LEVEL4"], 
                                              depth=4, Score=self.state.score)

        if (self.state.food_positions and 
            (not new_thief_position or [thief_row, thief_col] == new_thief_position)):
            new_thief_position = self.get_random_valid_move(thief_row, thief_col)
            
        return new_thief_position, result
        
    def start_game(self):
        police_new_positions = []
        result = []
        new_thief_position = []
        self.initialize_game_data()
        thief_can_move = True

        game_exit = False
        is_moving = False
        movement_timer = 0
        game_status = 0
        delay = 100

        while not game_exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.show_menu()
                    return

            if delay > 0:
                delay -= 1
                
            if delay <= 0:
                if is_moving:
                    movement_timer += 1 

                    if police_new_positions:
                        self.process_police_movement(police_new_positions, movement_timer)

                    if new_thief_position:
                        movement_done = self.process_thief_movement(new_thief_position, movement_timer)
                        if movement_done:
                            is_moving = False
                            new_thief_position = []

                    if self.check_collision_with_police():
                        thief_can_move = False
                        game_exit = True
                        game_status = -1

                    if not self.state.food_positions:
                        game_status = 1
                        game_exit = True

                    if movement_timer >= SIZE_WALL:
                        is_moving = False
                else:
                    if self.state.current_level == 3:
                        police_new_positions = self.generate_police_movements(movement_type=1)
                    elif self.state.current_level == 4:
                        police_new_positions = self.generate_police_movements(movement_type=2)
                    else:
                        police_new_positions = self.generate_police_movements(movement_type=0)

                    is_moving = True
                    movement_timer = 0

                    if not thief_can_move:
                        continue

                    [thief_row, thief_col] = self.state.thief_player.getRC()
                    new_thief_position, result = self.calculate_thief_move(thief_row, thief_col, result)
                        
                    if new_thief_position:
                        self.update_thief_direction(new_thief_position[0], new_thief_position[1])
                        if self.check_collision_with_police(new_thief_position[0], new_thief_position[1]):
                            thief_can_move = False
                            game_exit = True
                            game_status = -1

            self.screen.fill(BLACK)
            self.draw_game_objects()
            pygame.display.flip()
            self.clock.tick(FPS)

        self.handle_game_end(game_status)
        
    def handle_game_end(self, status):
        self.state.game_end_done = False
        lose_bg = pygame.image.load("images/gameover.png")
        lose_bg = pygame.transform.scale(lose_bg, (WIDTH, HEIGHT))
        win_bg = pygame.image.load("images/win1.png")
        win_bg = pygame.transform.scale(win_bg, (WIDTH, HEIGHT))

        def click_continue():
            self.state.game_end_done = True

        def click_quit():
            pygame.quit()
            sys.exit(0)

        btn_continue = Button(WIDTH // 2 - 300, HEIGHT // 2 - 50, 200, 100, self.screen, "CONTINUE", click_continue)
        btn_quit = Button(WIDTH // 2 + 50, HEIGHT // 2 - 50, 200, 100, self.screen, "QUIT", click_quit)

        delay = 100
        while not self.state.game_end_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            if delay > 0:
                delay -= 1
                pygame.display.flip()
                self.clock.tick(FPS)
                continue

            if status == -1:
                self.screen.blit(lose_bg, (0, 0))
            else:
                self.screen.blit(win_bg, (0, 0))
                score_text = self.large_font.render(f'Your Score: {self.state.score}', False, RED)
                self.screen.blit(score_text, (WIDTH // 4 - 65, 10))

            btn_quit.process()
            btn_continue.process()

            pygame.display.flip()
            self.clock.tick(FPS)

        self.show_menu()
        
    def show_menu(self):
        menu = Menu(self.screen)
        self.state.current_level, self.state.map_file_path = menu.run()
        self.start_game()


if __name__ == '__main__':
    game = GameManager()
    game.show_menu()
    pygame.quit()