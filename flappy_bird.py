# flappy bird game
import random
import pygame
import sys

pygame.init()

# okno
HEIGHT = 480
WIDTH = 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')

clock = pygame.time.Clock()
FPS = 60

# barvy
WHITE = (255, 255, 255)
SKY = (135, 206, 235)

BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)

YELLOW = (255, 230, 0)

BLACK = (0,0,0)
RED = (255,0,0)

# pták
bird_x = 100
bird_y = HEIGHT // 2
bird_radius = 20
bird_velocity = 0
gravity = 0.5
jump_strength = -10

# trubky
pipe_width = 80
pipe_gap = 150
pipes = []
pipe_spawn_timer = 0
pipe_spawn_interval = 1500  # ms
pipe_speed = 5

score = 0
font = pygame.font.SysFont('arial', 24, bold=True)

running = True

def reset_game():
    global bird_y, bird_velocity, pipes, pipe_spawn_timer, score, running
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    pipe_spawn_timer = 0
    score = 0
    running = True


def spawn_pipe():
    height = random.randint(50, HEIGHT - pipe_gap - 50)
    return {'x': WIDTH, 'height': height, 'passed': False}


def draw_pipe(pipe):
    x = pipe['x']
    h = pipe['height']

    top_rect = (x, 0, pipe_width, h)
    bottom_rect = (x, h + pipe_gap, pipe_width, HEIGHT - h - pipe_gap)

    pygame.draw.rect(screen, GREEN, top_rect)
    pygame.draw.rect(screen, GREEN, bottom_rect)

    pygame.draw.rect(screen, DARK_GREEN, top_rect, 5)
    pygame.draw.rect(screen, DARK_GREEN, bottom_rect, 5)


def check_collision(pipe):
    x = pipe['x']
    h = pipe['height']
    if (bird_x + bird_radius > x and bird_x - bird_radius < x + pipe_width and
            (bird_y - bird_radius < h or bird_y + bird_radius > h + pipe_gap)):
        return True
    return False


reset_game()

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump_strength

    # update bird
    bird_velocity += gravity
    bird_y += bird_velocity

    # spawn pipes
    pipe_spawn_timer += clock.get_time()
    if pipe_spawn_timer >= pipe_spawn_interval:
        pipe_spawn_timer = 0
        pipes.append(spawn_pipe())

    # update pipes
    for pipe in pipes:
        pipe['x'] -= pipe_speed

    # remove off-screen pipes
    pipes = [p for p in pipes if p['x'] + pipe_width > 0]

    # collision with ground/ceiling
    if bird_y + bird_radius > HEIGHT or bird_y - bird_radius < 0:
        running = False

    # collision with pipes & scoring
    for pipe in pipes:
        if check_collision(pipe):
            running = False
        if not pipe['passed'] and pipe['x'] + pipe_width < bird_x:
            pipe['passed'] = True
            score += 1

    # render
    screen.fill(SKY)
    # tělo ptáka
    pygame.draw.circle(screen, YELLOW, (bird_x, int(bird_y)), bird_radius)

    # oko
    pygame.draw.circle(screen, WHITE, (bird_x + 6, int(bird_y) - 6), 6)
    pygame.draw.circle(screen, BLACK, (bird_x + 7, int(bird_y) - 6), 3)

    for pipe in pipes:
        draw_pipe(pipe)

    score_text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    if not running:
        # jednoduchá obrazovka "game over"
        screen.fill(SKY)
        game_over_text = font.render('Game Over - Press R to restart or Q to quit', True, RED)
        score_text = font.render(f'Final Score: {score}', True, RED)
        screen.blit(game_over_text, (20, HEIGHT // 2 - 40))
        screen.blit(score_text, (20, HEIGHT // 2 + 10))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_r:
                        reset_game()
                        waiting = False

# ukončení hry
pygame.quit()
sys.exit()