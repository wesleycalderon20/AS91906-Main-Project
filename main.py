import pygame
import random

pygame.init()

# Constants
COLOR_BLACK = pygame.Color("black")
COLOR_WHITE = pygame.Color("white")
COLOR_RED   = pygame.Color("red")
COLOR_BLUE  = pygame.Color("blue")
# Main Menu background color
BACKGROUND_COLOR = pygame.Color('#c1ff72')
# Gameplay Checkerboard background color
CHECKERBOARD_EDGE = pygame.Color('#ff751f')
CHECKERBOARD_DARK = pygame.Color('#ff914d')
CHECKERBOARD_LIGHT = pygame.Color('#ffbd59')
BASE_COLOR = pygame.Color('#14ae5c')  
# Snake and Food Color
SNAKE_COLOR = pygame.Color('#7ed957')
FOOD_COLOR =  pygame.Color("#FFE600")
# Buttons hover color
HOVER_COLOR = pygame.Color("white")
# Main game Font
MAIN_FONT = 'freesansbold.ttf'
FONT_SIZE = 35

class Button:
    # User interface button component
    def __init__(self, x, y, w, h, text, border_color):
        self._rect = pygame.Rect(x, y, w, h)
        self._text = text
        self._border_color = border_color
        self._mouse_over = False
        self._button_down = False
        self.text_color = COLOR_BLACK
    # Buttons action when clicked
    def set_action(self, action_function):
        if callable(action_function):
            self._action = action_function
    # Movement of mouse 
    def mouse_move(self, mouse_x, mouse_y):
        self._mouse_over = self._rect.collidepoint(mouse_x, mouse_y)
    # Button moves down when clicked and moves up after clicked
    def mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._mouse_over:
                self._button_down = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._button_down = False

    def draw(self, surface):
        # Draw the button layout
        # Hover color button when pressed
        current_color = HOVER_COLOR if self._mouse_over else BASE_COLOR # conditional expression
        pygame.draw.rect(surface, current_color, self._rect, self._rect.height // 2)
        font = pygame.font.Font(MAIN_FONT, FONT_SIZE)
        text_surf = font.render(self._text, True, self.text_color)
        text_rect = text_surf.get_rect()
        text_rect.center = self._rect.center
        if self._button_down:
            text_rect.x += 4
            text_rect.y += 4
        surface.blit(text_surf, text_rect)

# Main Menu Buttons and Title customise
class MenuButtons:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.buttons = []
        self.menu_buttons()
    # Game title background layout for main menu
    def game_title(self, surface):
        TITLE_Y = 100
        TITLE_X = 190
        BORDER_X = 370
        BORDER_Y = 100
        BORDER_SIZE = 5
        OFFSET_X = 1
        OFFSET_Y = -2
        # Background color for Main Menu
        surface.fill(BACKGROUND_COLOR)
        title_font = pygame.font.Font(MAIN_FONT, 100)
        title_surf = title_font.render(" Snake ", True, COLOR_BLACK)
        pygame.draw.rect(title_surf, COLOR_BLACK, (OFFSET_X, OFFSET_Y, BORDER_X, BORDER_Y), BORDER_SIZE)
        surface.blit(title_surf, (self.screen_w // 2 - TITLE_X, TITLE_Y))
        for btn in self.buttons:
            btn.draw(surface)
    # Main menu button customisation 
    def menu_buttons(self):
        # Constants for buttons
        BTN_W = 220
        BTN_H = 60
        START_Y = 260
        SPACING = 80
        POS_X = (self.screen_w // 2) - (BTN_W // 2)
        # Draw Main Menu Buttons
        menu_items = [("Play", "play"), ("Settings", "settings"), ("Exit", "exit")]
        for i, (label, icon) in enumerate(menu_items):
            y_pos = START_Y + (i * SPACING)
            button = Button(POS_X, y_pos, BTN_W, BTN_H, label, icon)
            self.buttons.append(button)

# Gameplay layout
class GamePlay:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
    # background checkerboard size layout
        self.background_x = 17
        self.background_y = 17
        self.cell_size = 25
     # Center the grid on screen horizontally, push down for header UI
        self.grid_x = (self.screen_w - (self.background_x * self.cell_size)) // 2
        self.grid_y = 110
        EXIT_BTN_X = 65
        EXIT_BTN_Y = 30
        EXIT_BTN_WIDTH = 35
        EXIT_BTN_HEIGHT = 35
    # Top-right Exit Icon
        self.exit_btn_rect = pygame.Rect(self.screen_w - EXIT_BTN_X, EXIT_BTN_Y, EXIT_BTN_WIDTH, EXIT_BTN_HEIGHT)
        self.high_score = 0
        self.reset_game()
    def reset_game(self):
        self.score = 0
    # Starting positioning of snake
    # [x, y] coordinates of the body of snake
        self.snake = [[7, 5], [6, 5], [5, 5], [4, 5]]
        self.direction = [1, 0]
        self.next_direction = [1, 0]
        self.spawn_food()
        self.game_over = False
    def spawn_food(self):
        while True:
            self.food = [random.randint(0, self.background_x - 1), random.randint(0, self.background_y - 1)]
            if self.food in self.snake:
                continue
            break
    # snake movement Key controller
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != [0, 1]:
                self.next_direction = [0, -1]
            elif event.key == pygame.K_DOWN and self.direction != [0, -1]:
                self.next_direction = [0, 1]
            elif event.key == pygame.K_LEFT and self.direction != [1, 0]:
                self.next_direction = [-1, 0]
            elif event.key == pygame.K_RIGHT and self.direction != [-1, 0]:
                self.next_direction = [1, 0]
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.exit_btn_rect.collidepoint(event.pos):
                return "menu"
        return "playing"
    def update(self):
        if self.game_over:
            return
        self.direction = self.next_direction
    # new head position
        new_head = [self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1]]
    # Boundary Wall Collision
        if new_head[0] < 0 or new_head[0] >= self.background_x - 0 or new_head[1] < 0 or new_head[1] >= self.background_y - 0:
            self.game_over = True
            return
    # body collision
        if new_head in self.snake:
            self.game_over = True
            return
    # Advance snake
        self.snake.insert(0, new_head)
    # Food Collection Score
        if new_head == self.food:
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
            self.spawn_food()
        else:
            self.snake.pop()
    def draw(self, surface):
    # Gameplay background fill
    # Draw Gameplay Top Icons
        surface.fill(CHECKERBOARD_EDGE)
        FONT = pygame.font.Font(MAIN_FONT, FONT_SIZE)
        SCORE_X = 115
        SCORE_Y = 35
    # Score Icon layout (Current Score)
        FOOD_SCORE_SIZE = 15
        FOOD_SCORE_X = 100
        FOOD_SCORE_Y = 50
        pygame.draw.circle(surface, FOOD_COLOR, (FOOD_SCORE_X, FOOD_SCORE_Y), FOOD_SCORE_SIZE)
        pygame.draw.circle(surface, COLOR_BLACK, (FOOD_SCORE_X, FOOD_SCORE_Y), FOOD_SCORE_SIZE, 2)
        score_txt = FONT.render(f": {self.score}", True, COLOR_BLACK)
        surface.blit(score_txt, (SCORE_X, SCORE_Y))
     # Tophy Icon (High Score)
        TROPHY_X = 350
        TROPHY_Y = 30
        pygame.draw.rect(surface, COLOR_BLACK, (TROPHY_X, TROPHY_Y + 6, 18, 15)), \
        pygame.draw.rect(surface, COLOR_BLACK, (TROPHY_X + 6, TROPHY_Y + 20, 6, 10)), \
        pygame.draw.rect(surface, COLOR_BLACK, (TROPHY_X + 2, TROPHY_Y + 28, 14, 7))
        high_score = FONT.render(f": {self.high_score}", True, COLOR_BLACK)
        surface.blit(high_score, (370, 35))
    # Exit (X) Icon Layout 
        pygame.draw.line(surface, COLOR_BLACK, (self.exit_btn_rect.left, self.exit_btn_rect.top), (self.exit_btn_rect.right, self.exit_btn_rect.bottom), 10)
        pygame.draw.line(surface, COLOR_BLACK, (self.exit_btn_rect.left, self.exit_btn_rect.bottom), (self.exit_btn_rect.right, self.exit_btn_rect.top), 10)
    # Checkerboard Main Menu background Pattern Color
        for r in range(self.background_y):
            for c in range(self.background_x):
                cell_rect = pygame.Rect(self.grid_x + (c * self.cell_size), self.grid_y + (r * self.cell_size), self.cell_size, self.cell_size)
                current_cell_color = CHECKERBOARD_LIGHT if (r + c) % 2 == 0 else CHECKERBOARD_DARK
                pygame.draw.rect(surface, current_cell_color, cell_rect)
    # Draw game food
        food_rx = self.grid_x + (self.food[0] * self.cell_size) + self.cell_size // 2
        food_ry = self.grid_y + (self.food[1] * self.cell_size) + self.cell_size // 2
        pygame.draw.circle(surface, FOOD_COLOR, (food_rx, food_ry), 12)
        pygame.draw.circle(surface, COLOR_BLACK, (food_rx, food_ry), 12, 2)
        for index, segment in enumerate(self.snake):
            seg_x = self.grid_x + (segment[0] * self.cell_size)
            seg_y = self.grid_y + (segment[1] * self.cell_size)
            seg_rect = pygame.Rect(seg_x, seg_y, self.cell_size, self.cell_size)
        # Snake's body color and border
            pygame.draw.rect(surface, SNAKE_COLOR, seg_rect, border_radius=8)
            pygame.draw.rect(surface, COLOR_BLACK, seg_rect, 2, border_radius=8)
        # Head detail additions (Eyes)
            if index == 0:
                EYE_RADIUS = 5
            # Dynamically offset eyes depending on travel direction
                if self.direction == [1, 0] or self.direction == [-1, 0]: 
                # Horizontal Eyes
                    pygame.draw.circle(surface, COLOR_BLACK, (seg_rect.centerx, seg_rect.top + 7), EYE_RADIUS)
                    pygame.draw.circle(surface, COLOR_BLACK, (seg_rect.centerx, seg_rect.bottom - 7), EYE_RADIUS)
                else: 
                # Vertical Eyes
                    pygame.draw.circle(surface, COLOR_BLACK, (seg_rect.left + 7, seg_rect.centery), EYE_RADIUS)
                    pygame.draw.circle(surface, COLOR_BLACK, (seg_rect.right - 7, seg_rect.centery), EYE_RADIUS)
    # Game Over Screen
        if self.game_over:
        # fill background color with darkgreen when the game is over
        # GAME OVER title 
            surface.fill("darkgreen")
            gameover_font = pygame.font.Font(MAIN_FONT, 75)
            gameover_surf = gameover_font.render(" GAME OVER ", True, COLOR_RED)
            gameover_rect = gameover_surf.get_rect(center=(self.screen_w // 2, self.screen_h // 2 - 75))
        # Display the user's score when game is over
            score_font = pygame.font.Font(MAIN_FONT, 45)
            sub_score = score_font.render(f" Total Score: {self.score} ", True, COLOR_BLACK)
            sub_score_rect = sub_score.get_rect(center = (self.screen_w // 2, self.screen_h // 2 + 10))
        # Let the user to restart the game but resets the score and record the high score
            sub_font = pygame.font.Font(MAIN_FONT, 30)
            sub_surf = sub_font.render(" Press [R] to Restart ", True, COLOR_BLACK)
            sub_rect = sub_surf.get_rect(center=(self.screen_w // 2, self.screen_h // 2 + 75))
            surface.blit(gameover_surf, gameover_rect)
            surface.blit(sub_score, sub_score_rect)
            surface.blit(sub_surf, sub_rect)
        # Draw (X) Exit icon on top-right of Game Over Screen
            pygame.draw.line(surface, COLOR_BLACK, (self.exit_btn_rect.left, self.exit_btn_rect.top), (self.exit_btn_rect.right, self.exit_btn_rect.bottom), 10)
            pygame.draw.line(surface, COLOR_BLACK, (self.exit_btn_rect.left, self.exit_btn_rect.bottom), (self.exit_btn_rect.right, self.exit_btn_rect.top), 10)

# Main Menu screen adjustment and buttons input
class MainMenu:
    def __init__(self):
        self.snakes_speed = 120 # Snakes normal speed
        BUTTON_1 = 0
        BUTTON_2 = 0
        BUTTON_3 = 0
        BUTTON_4 = 0
        SCREEN_WIDTH = 600
        SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = "menu"
        self.game_started = False
        self.SNAKE_UPDATE_EVENT = pygame.USEREVENT
        pygame.time.set_timer(self.SNAKE_UPDATE_EVENT, self.snakes_speed)
        self.main_menu = MenuButtons(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.gameplay = GamePlay(SCREEN_WIDTH, SCREEN_HEIGHT)
    # Provide game mode buttons
        self.settings_buttons = []
        settings_items = [("Easy", "easy"), ("Normal", "normal"), ("Hard", "hard"), ("Menu", "menu")]
        for label, icon in settings_items:
        # Structuring placeholders; coordinates will re-center dynamically in the draw step
            self.settings_buttons.append(Button(BUTTON_1, BUTTON_2, BUTTON_3, BUTTON_4, label, icon))
    def run(self):
        while self.running:
            coords = pygame.mouse.get_pos()
        # Dynamic retrieval of current dimensions to catch Fullscreen / Resize updates
            minimise_w, minimise_h = self.screen.get_size()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.current_state == "menu":
                    if event.type == pygame.MOUSEMOTION:
                        for button in self.main_menu.buttons:
                            button.mouse_move(coords[0], coords[1])
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for button in self.main_menu.buttons:
                            button.mouse_click(event) 
                    if event.type == pygame.MOUSEBUTTONUP:
                        for button in self.main_menu.buttons:
                            was_down = button._button_down
                            was_over = button._mouse_over
                            button.mouse_click(event)
                            if was_down and was_over:
                                if button._text == "Play":
                                    self.gameplay.reset_game()
                                    self.game_started = False
                                    self.current_state = "playing"
                                elif button._text == "Settings":
                                    self.current_state = "settings_screen"
                                elif button._text == "Exit":
                                    self.running = False
            # Settings screen layout
                elif self.current_state == "settings_screen":
                    if event.type == pygame.MOUSEMOTION:
                        for button in self.settings_buttons:
                            button.mouse_move(coords[0], coords[1])  
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for button in self.settings_buttons:
                            button.mouse_click(event)
                    if event.type == pygame.MOUSEBUTTONUP:
                        for button in self.settings_buttons:
                            was_down = button._button_down
                            was_over = button._mouse_over
                            button.mouse_click(event)
                            if was_down and was_over:
                                if button._text == "Easy": # Slower speed
                                    self.snakes_speed = 180  
                                    pygame.time.set_timer(self.SNAKE_UPDATE_EVENT, self.snakes_speed)
                                    print("Game Mode set to EASY") # Remind the player where game mode sets to
                                elif button._text == "Normal": # Balanced speed
                                    self.snakes_speed = 120  
                                    pygame.time.set_timer(self.SNAKE_UPDATE_EVENT, self.snakes_speed)
                                    print("Game Mode set to NORMAL") # Remind the player where game mode sets to
                                elif button._text == "Hard": # Faster speed
                                    self.snakes_speed = 70   
                                    pygame.time.set_timer(self.SNAKE_UPDATE_EVENT, self.snakes_speed)
                                    print("Game Mode set to HARD") # Remind the player where game mode sets to
                                elif button._text == "Menu": # Go to main menu screen
                                    self.current_state = "menu"
            # Snake controlers
                elif self.current_state == "playing":
                # Check if a directional button is pressed to unpause the gameplay
                    if event.type == pygame.KEYDOWN:
                        if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d): # Key buttons controllers
                            self.game_started = True
                    next_state = self.gameplay.handle_input(event)
                    if next_state == "menu":
                        self.current_state = "menu"
                # Keyboard action handling if dead to restart game instance
                    if self.gameplay.game_over and event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.gameplay.reset_game()
                            self.game_started = False
                    if event.type == self.SNAKE_UPDATE_EVENT and self.game_started:
                        self.gameplay.update()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.current_state = "menu"
        # Layout Switch Board Rendering Engine Router
            if self.current_state == "menu":
                self.main_menu.screen_w = minimise_w
                self.main_menu.screen_h = minimise_h
            # Main Menu Buttons customisation
                BUTTON_X = 220
                BUTTON_Y = 260
                SPACING = 80
                POSITION_X = (minimise_w // 2) - (BUTTON_X // 2)
                for i, button in enumerate(self.main_menu.buttons):
                    button._rect.x = POSITION_X
                    button._rect.y = BUTTON_Y + (i * SPACING)
                self.main_menu.game_title(self.screen)
            elif self.current_state == "playing":
                self.screen.fill('Black')
                game_surf = pygame.Surface((self.gameplay.screen_w, self.gameplay.screen_h))
                self.gameplay.draw(game_surf)
            # Minimise screen adjustment
                scale_w = minimise_w / self.gameplay.screen_w
                scale_h = minimise_h / self.gameplay.screen_h
                scale_factor = min(scale_w, scale_h)
            # Full Screen adjustment
                fullscreen_w = int(self.gameplay.screen_w * scale_factor)
                fullscreen_h = int(self.gameplay.screen_h * scale_factor)
                scaled_surf = pygame.transform.smoothscale(game_surf, (fullscreen_w, fullscreen_h))
                render_x = (minimise_w - fullscreen_w) // 2
                render_y = (minimise_h - fullscreen_h) // 2
                self.screen.blit(scaled_surf, (render_x, render_y))
            elif self.current_state == "settings_screen":
            # Keep matching background colors
                self.screen.fill(BACKGROUND_COLOR)
            # Settings input (Header Adjustment)
            # Constants for game mode buttons
                SETTINGS_BORDER_X = 365
                SETTINGS_BORDER_Y = 50
                SETTINS_BORDER_SIZE = 3
                SETTINGS_OFFSET_X = 1
                SETTINGS_OFFSET_Y = -1
                settings_font = pygame.font.Font(MAIN_FONT, 55)
                settings_surf = settings_font.render(" Select Mode ", True, COLOR_BLACK) # Asking user to choose game mode
                pygame.draw.rect(settings_surf, COLOR_BLACK, (SETTINGS_OFFSET_X, SETTINGS_OFFSET_Y, SETTINGS_BORDER_X, SETTINGS_BORDER_Y), SETTINS_BORDER_SIZE)
                text_rect = settings_surf.get_rect(center=(minimise_w // 2, 100))
                self.screen.blit(settings_surf, text_rect)
            # Game mode buttons adjustment
                SETTINGS_BTN_W = 220
                SETTINGS_BTN_H = 50
                SETTINGS_BTN_Y = 200
                DIFFICULT_SPACING = 80
                SETTINGS_BTN_X = (minimise_w // 2) - (SETTINGS_BTN_W // 2)
                for i, button in enumerate(self.settings_buttons):
                    button._rect.x = SETTINGS_BTN_X
                    button._rect.y = SETTINGS_BTN_Y + (i * DIFFICULT_SPACING)
                    button._rect.width = SETTINGS_BTN_W
                    button._rect.height = SETTINGS_BTN_H
                # Snake Speeds adjustment
                    if button._text == "Easy" and self.snakes_speed == 180: # Slow speed
                        button.hover_color = HOVER_COLOR # Hover when buttons being pressed
                    elif button._text == "Normal" and self.snakes_speed == 120: # Normal Speed
                        button.hover_color = HOVER_COLOR
                    elif button._text == "Hard" and self.snakes_speed == 70: # Fast speed
                        button.hover_color = HOVER_COLOR
                    else:
                        button.hover_color = COLOR_WHITE
                    button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(360)

if __name__ == "__main__":
    gameplay = MainMenu()
    gameplay.run()