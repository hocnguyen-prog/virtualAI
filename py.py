import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bloxorz - Animace Valení")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 28)
big_font = pygame.font.SysFont("consolas", 48, bold=True)

# Barvy
SKY = (8, 12, 35)
TILE = (65, 65, 85)
TILE_EDGE = (100, 100, 120)
GOAL = (255, 220, 60)
BLOCK_COLOR = (210, 40, 40)
BLOCK_EDGE = (255, 100, 100)

# Level
level = [
    [0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,0,0,0],
    [0,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,0],
    [0,1,1,1,2,1,1,1,0],
    [0,1,1,1,1,1,1,1,0],
    [0,0,1,1,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0]
]

ROWS, COLS = len(level), len(level[0])

# Globální stav bloku
block_x = 2
block_y = 2
orientation = 2          # 0 = leží X, 1 = leží Y, 2 = stojí

# Animace
animating = False
anim_progress = 0.0
anim_speed = 0.20
start_x = start_y = 0.0
target_x = target_y = 0.0
start_orient = 0
roll_angle = 0
roll_dir = (0, 0)

moves = 0


def is_valid(x, y):
    if not (0 <= x < COLS and 0 <= y < ROWS):
        return False
    return level[y][x] != 0


def start_animation(dx, dy):
    global block_x, block_y, orientation, animating, anim_progress
    global start_x, start_y, target_x, target_y, start_orient, roll_dir, roll_angle

    start_x = float(block_x)
    start_y = float(block_y)
    start_orient = orientation
    roll_dir = (dx, dy)
    roll_angle = 0
    anim_progress = 0.0
    animating = True

    # Výpočet nové pozice a orientace
    if orientation == 2:                    # stojí → padá
        if dx != 0:
            orientation = 0
            block_x += dx
        else:
            orientation = 1
            block_y += dy
    elif orientation == 0:                  # leží podél X
        if dx != 0:
            block_x += dx * 2
        else:
            orientation = 2
            block_y += dy
    elif orientation == 1:                  # leží podél Y
        if dy != 0:
            block_y += dy * 2
        else:
            orientation = 2
            block_x += dx

    target_x = float(block_x)
    target_y = float(block_y)


def update_animation(dt):
    global anim_progress, roll_angle, animating, moves

    if not animating:
        return False

    anim_progress += dt * 4.5          # rychlost animace

    if anim_progress >= 1.0:
        anim_progress = 1.0
        animating = False
        moves += 1
        roll_angle = 0
        return True

    # Rotace bloku
    roll_angle = -90 * anim_progress if (roll_dir[0] > 0 or roll_dir[1] > 0) else 90 * anim_progress
    return False


def draw_tile(x, y, tile_type):
    if tile_type == 0:
        return
    sx = 250 + x * 60
    sy = 120 + y * 60
    color = GOAL if tile_type == 2 else TILE
    pygame.draw.rect(screen, color, (sx, sy, 58, 58), border_radius=10)
    pygame.draw.rect(screen, TILE_EDGE, (sx, sy, 58, 58), 4, border_radius=10)


def draw_block():
    global roll_angle

    # Interpolace pozice
    if animating:
        x = start_x + (target_x - start_x) * anim_progress
        y = start_y + (target_y - start_y) * anim_progress
    else:
        x = float(block_x)
        y = float(block_y)

    bx = 250 + x * 60
    by = 120 + y * 60

    if orientation == 2:                                 # Stojí
        pygame.draw.rect(screen, BLOCK_COLOR, (bx + 8, by + 8, 44, 44), border_radius=8)
        pygame.draw.rect(screen, BLOCK_EDGE, (bx + 8, by + 8, 44, 44), 5, border_radius=8)
        
    elif orientation == 0:                               # Leží na X
        pygame.draw.rect(screen, BLOCK_COLOR, (bx - 28, by + 9, 118, 42), border_radius=10)
        pygame.draw.rect(screen, BLOCK_EDGE, (bx - 28, by + 9, 118, 42), 6, border_radius=10)
        
    else:                                                # Leží na Y
        pygame.draw.rect(screen, BLOCK_COLOR, (bx + 9, by - 28, 42, 118), border_radius=10)
        pygame.draw.rect(screen, BLOCK_EDGE, (bx + 9, by - 28, 42, 118), 6, border_radius=10)


# ====================== HLAVNÍ SMYČKA ======================
running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not animating:
            if event.key in (pygame.K_UP, pygame.K_w):
                start_animation(0, -1)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                start_animation(0, 1)
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                start_animation(-1, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                start_animation(1, 0)
            elif event.key == pygame.K_r:
                block_x, block_y = 2, 2
                orientation = 2
                moves = 0
                animating = False

    if animating:
        update_animation(dt)

    screen.fill(SKY)

    # Kreslení levelu
    for y in range(ROWS):
        for x in range(COLS):
            draw_tile(x, y, level[y][x])

    draw_block()

    # Výhra
    if not animating and orientation == 2 and level[block_y][block_x] == 2:
        win = big_font.render("VÝBORNĚ! VYHRÁL JSI!", True, (255, 220, 60))
        screen.blit(win, (WIDTH//2 - win.get_width()//2, 80))

    # UI
    moves_text = font.render(f"Tahy: {moves}", True, (200, 220, 255))
    screen.blit(moves_text, (30, 20))
    
    controls = font.render("WASD / Šipky = pohyb    R = restart", True, (170, 170, 200))
    screen.blit(controls, (30, HEIGHT - 45))

    pygame.display.flip()

pygame.quit()
sys.exit()