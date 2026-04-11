
# snake game example using pygame
import pygame
import random
import sys

# initialize pygame
pygame.init()

# set up the display
WIDTH, HEIGHT = 640, 480
NORMAL_CELL_SIZE = 20
BIG_CELL_SIZE = 40
CELL_SIZE = NORMAL_CELL_SIZE
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# set up fonts
font = pygame.font.SysFont('arial', 24, bold=True)
small_font = pygame.font.SysFont('arial', 18)

# game state
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
direction = (1, 0)
food = None
clock = pygame.time.Clock()
snake_speed = 10
score = 0
running = True
big_mode = False
leaderboard = []

# helper functions

def set_mode(is_big):
    global CELL_SIZE, GRID_WIDTH, GRID_HEIGHT
    CELL_SIZE = BIG_CELL_SIZE if is_big else NORMAL_CELL_SIZE
    GRID_WIDTH = WIDTH // CELL_SIZE
    GRID_HEIGHT = HEIGHT // CELL_SIZE


def draw_rect_grid(color, position):
    x, y = position
    pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))


def spawn_food(snake_body):
    while True:
        food_pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if food_pos not in snake_body:
            return food_pos


def draw_text(text, color, x, y, font_obj=font):
    surface = font_obj.render(text, True, color)
    screen.blit(surface, (x, y))


def add_to_leaderboard(score):
    global leaderboard
    leaderboard.append(score)
    leaderboard = sorted(leaderboard, reverse=True)[:5]


def draw_leaderboard():
    draw_text('Leaderboard:', YELLOW, WIDTH - 220, 10)
    for i, s in enumerate(leaderboard):
        draw_text(f'{i + 1}. {s}', WHITE, WIDTH - 220, 40 + 24 * i, small_font)


def game_over_screen(score):
    add_to_leaderboard(score)
    screen.fill(BLACK)
    draw_text('GAME OVER', RED, WIDTH // 2 - 100, HEIGHT // 2 - 80)
    draw_text(f'Final Score: {score}', WHITE, WIDTH // 2 - 90, HEIGHT // 2 - 40)
    draw_text(f'Current Mode: {"BIG" if big_mode else "Normal"}', WHITE, WIDTH // 2 - 90, HEIGHT // 2 - 10)
    draw_text('Press R to restart, Q to quit, M to toggle mode', WHITE, WIDTH // 2 - 220, HEIGHT // 2 + 30)

    for i, s in enumerate(leaderboard):
        draw_text(f'{i + 1}. {s}', YELLOW, WIDTH // 2 - 50, HEIGHT // 2 + 70 + 26 * i, small_font)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    return 'restart'
                if event.key == pygame.K_m:
                    return 'toggle_mode'


def reset_game():
    global snake, direction, food, snake_speed, score, running
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)
    food = spawn_food(snake)
    snake_speed = 10
    score = 0
    running = True


set_mode(big_mode)
reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if direction != (0, 1):
                    direction = (0, -1)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if direction != (0, -1):
                    direction = (0, 1)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if direction != (1, 0):
                    direction = (-1, 0)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if direction != (-1, 0):
                    direction = (1, 0)

    if not running:
        result = game_over_screen(score)
        if result == 'toggle_mode':
            big_mode = not big_mode
            set_mode(big_mode)
        reset_game()

    # move snake
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    # collision with walls
    if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
        running = False

    # collision with self
    if new_head in snake:
        running = False

    if not running:
        continue

    snake.insert(0, new_head)

    # eating food
    if new_head == food:
        score += 1
        food = spawn_food(snake)
        if score % 5 == 0:
            snake_speed += 1
    else:
        snake.pop()

    # draw everything
    screen.fill(BLACK)

    for segment in snake:
        draw_rect_grid(GREEN, segment)

    draw_rect_grid(RED, food)

    draw_text(f'Score: {score}', WHITE, 10, 10)
    draw_text(f'Speed: {snake_speed}', WHITE, 10, 30)
    draw_text(f'Mode: {"BIG" if big_mode else "Normal"}', WHITE, 10, 50)
    draw_leaderboard()

    pygame.display.flip()
    clock.tick(snake_speed)

# snake game example using pygame
import pygame
import random
import sys

# initialize pygame
pygame.init()

# set up the display
WIDTH, HEIGHT = 640, 480
NORMAL_CELL_SIZE = 20
BIG_CELL_SIZE = 40
CELL_SIZE = NORMAL_CELL_SIZE
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# set up fonts
font = pygame.font.SysFont('arial', 24, bold=True)
small_font = pygame.font.SysFont('arial', 18)

# game state
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
direction = (1, 0)
food = None
clock = pygame.time.Clock()
snake_speed = 10
score = 0
running = True
big_mode = False
leaderboard = []

# helper functions

def set_mode(is_big):
    global CELL_SIZE, GRID_WIDTH, GRID_HEIGHT
    CELL_SIZE = BIG_CELL_SIZE if is_big else NORMAL_CELL_SIZE
    GRID_WIDTH = WIDTH // CELL_SIZE
    GRID_HEIGHT = HEIGHT // CELL_SIZE


def draw_rect_grid(color, position):
    x, y = position
    pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))


def spawn_food(snake_body):
    while True:
        food_pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if food_pos not in snake_body:
            return food_pos


def draw_text(text, color, x, y, font_obj=font):
    surface = font_obj.render(text, True, color)
    screen.blit(surface, (x, y))


def add_to_leaderboard(score):
    global leaderboard
    leaderboard.append(score)
    leaderboard = sorted(leaderboard, reverse=True)[:5]


def draw_leaderboard():
    draw_text('Leaderboard:', YELLOW, WIDTH - 220, 10)
    for i, s in enumerate(leaderboard):
        draw_text(f'{i + 1}. {s}', WHITE, WIDTH - 220, 40 + 24 * i, small_font)


def game_over_screen(score):
    add_to_leaderboard(score)
    screen.fill(BLACK)
    draw_text('GAME OVER', RED, WIDTH // 2 - 100, HEIGHT // 2 - 80)
    draw_text(f'Final Score: {score}', WHITE, WIDTH // 2 - 90, HEIGHT // 2 - 40)
    draw_text(f'Current Mode: {"BIG" if big_mode else "Normal"}', WHITE, WIDTH // 2 - 90, HEIGHT // 2 - 10)
    draw_text('Press R to restart, Q to quit, M to toggle mode', WHITE, WIDTH // 2 - 220, HEIGHT // 2 + 30)

    for i, s in enumerate(leaderboard):
        draw_text(f'{i + 1}. {s}', YELLOW, WIDTH // 2 - 50, HEIGHT // 2 + 70 + 26 * i, small_font)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    return 'restart'
                if event.key == pygame.K_m:
                    return 'toggle_mode'


def reset_game():
    global snake, direction, food, snake_speed, score, running
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)
    food = spawn_food(snake)
    snake_speed = 10
    score = 0
    running = True


set_mode(big_mode)
reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if direction != (0, 1):
                    direction = (0, -1)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if direction != (0, -1):
                    direction = (0, 1)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if direction != (1, 0):
                    direction = (-1, 0)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if direction != (-1, 0):
                    direction = (1, 0)

    if not running:
        result = game_over_screen(score)
        if result == 'toggle_mode':
            big_mode = not big_mode
            set_mode(big_mode)
        reset_game()

    # move snake
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    # collision with walls
    if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
        running = False

    # collision with self
    if new_head in snake:
        running = False

    if not running:
        continue

    snake.insert(0, new_head)

    # eating food
    if new_head == food:
        score += 1
        food = spawn_food(snake)
        if score % 5 == 0:
            snake_speed += 1
    else:
        snake.pop()

    # draw everything
    screen.fill(BLACK)

    for segment in snake:
        draw_rect_grid(GREEN, segment)

    draw_rect_grid(RED, food)

    draw_text(f'Score: {score}', WHITE, 10, 10)
    draw_text(f'Speed: {snake_speed}', WHITE, 10, 30)
    draw_text(f'Mode: {"BIG" if big_mode else "Normal"}', WHITE, 10, 50)
    draw_leaderboard()

    pygame.display.flip()
    clock.tick(snake_speed)
    import pygame
import time
import random