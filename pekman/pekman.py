import pygame
import sys
import random
import math   # ← přidáno pro radians

pygame.init()

# Barvy
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

TILE_SIZE = 20
COLS = 28
ROWS = 31
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE + 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pekman")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Bludiště (31 řádků)
maze = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
[1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1],
[1,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1],
[1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1],
[1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1],
[1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1],
[1,1,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1],
[1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1],
[1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
[1,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1],
[1,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1],
[1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
[1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1],
[1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
[1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

dots = [(x, y) for y in range(ROWS) for x in range(COLS) if maze[y][x] == 0]

class Pekman:
    def __init__(self):
        self.x = 14 * TILE_SIZE
        self.y = 23 * TILE_SIZE
        self.speed = 3
        self.dir = (0, 0)
        self.next_dir = (0, 0)
        self.radius = TILE_SIZE // 2 - 2
        self.mouth_angle = 0

    def update(self):
        if self.next_dir != (0, 0):
            nx = self.x + self.next_dir[0] * self.speed
            ny = self.y + self.next_dir[1] * self.speed
            if self.can_move(nx, ny):
                self.dir = self.next_dir

        new_x = self.x + self.dir[0] * self.speed
        new_y = self.y + self.dir[1] * self.speed

        if self.can_move(new_x, new_y):
            self.x = new_x
            self.y = new_y

        # Tunely
        if self.x < -TILE_SIZE: self.x = WIDTH
        elif self.x > WIDTH: self.x = -TILE_SIZE

    def can_move(self, new_x, new_y):
        r = self.radius
        positions = [(new_x-r, new_y-r), (new_x+r, new_y-r),
                     (new_x-r, new_y+r), (new_x+r, new_y+r)]
        for px, py in positions:
            gx = int(px // TILE_SIZE)
            gy = int(py // TILE_SIZE)
            if not (0 <= gx < COLS and 0 <= gy < ROWS) or maze[gy][gx] == 1:
                return False
        return True

    def draw(self):
        self.mouth_angle = (self.mouth_angle + 8) % 40
        angle = 30 + abs(self.mouth_angle - 20)

        cx, cy = int(self.x), int(self.y)

        if self.dir == (1, 0):    # vpravo
            start, stop = angle, 360 - angle
        elif self.dir == (-1, 0): # vlevo
            start, stop = 180 + angle, 540 - angle
        elif self.dir == (0, -1): # nahoru
            start, stop = 270 + angle, 630 - angle
        elif self.dir == (0, 1):  # dolů
            start, stop = 90 + angle, 450 - angle
        else:
            start, stop = 0, 360

        pygame.draw.circle(screen, YELLOW, (cx, cy), self.radius)
        pygame.draw.arc(screen, BLACK,
                        (cx - self.radius, cy - self.radius, self.radius*2, self.radius*2),
                        math.radians(start), math.radians(stop), self.radius)   # ← opraveno

class Ghost:
    def __init__(self, color, x, y):
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.color = color
        self.speed = 2
        self.dir = random.choice([(1,0), (-1,0), (0,1), (0,-1)])

    def update(self):
        if random.random() < 0.05:
            self.dir = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        new_x = self.x + self.dir[0] * self.speed
        new_y = self.y + self.dir[1] * self.speed
        if self.can_move(new_x, new_y):
            self.x = new_x
            self.y = new_y

    def can_move(self, new_x, new_y):
        r = TILE_SIZE//2 - 4
        for px, py in [(new_x-r,new_y-r),(new_x+r,new_y-r),(new_x-r,new_y+r),(new_x+r,new_y+r)]:
            gx = int(px // TILE_SIZE)
            gy = int(py // TILE_SIZE)
            if not (0 <= gx < COLS and 0 <= gy < ROWS) or maze[gy][gx] == 1:
                return False
        return True

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), TILE_SIZE//2 - 2)
        pygame.draw.circle(screen, WHITE, (int(self.x)-6, int(self.y)-5), 5)
        pygame.draw.circle(screen, WHITE, (int(self.x)+6, int(self.y)-5), 5)
        pygame.draw.circle(screen, BLACK, (int(self.x)-6, int(self.y)-5), 2)
        pygame.draw.circle(screen, BLACK, (int(self.x)+6, int(self.y)-5), 2)

# Objekty
player = Pekman()
ghosts = [
    Ghost(RED, 13, 11),
    Ghost((255, 184, 255), 14, 11),
    Ghost((0, 255, 255), 13, 12),
    Ghost((255, 165, 0), 14, 12)
]

score = 0
game_over = False
win = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:  player.next_dir = (1, 0)
            elif event.key == pygame.K_LEFT: player.next_dir = (-1, 0)
            elif event.key == pygame.K_UP:   player.next_dir = (0, -1)
            elif event.key == pygame.K_DOWN: player.next_dir = (0, 1)

    if not game_over and not win:
        player.update()

        gx = int(player.x // TILE_SIZE)
        gy = int(player.y // TILE_SIZE)
        if (gx, gy) in dots:
            dots.remove((gx, gy))
            score += 10

        for ghost in ghosts:
            ghost.update()
            if abs(player.x - ghost.x) < TILE_SIZE - 8 and abs(player.y - ghost.y) < TILE_SIZE - 8:
                game_over = True

        if len(dots) == 0:
            win = True

    # Kreslení
    screen.fill(BLACK)

    for y in range(ROWS):
        for x in range(COLS):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLUE, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

    for x, y in dots:
        pygame.draw.circle(screen, WHITE, (x*TILE_SIZE + TILE_SIZE//2, y*TILE_SIZE + TILE_SIZE//2), 4)

    player.draw()
    for ghost in ghosts:
        ghost.draw()

    score_text = font.render(f"Skóre: {score}", True, WHITE)
    screen.blit(score_text, (20, HEIGHT - 45))

    if game_over:
        txt = font.render("GAME OVER", True, RED)
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2))
    elif win:
        txt = font.render("VYHRÁL JSI!!!", True, YELLOW)
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()