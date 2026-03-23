<<<<<<< HEAD
import pygame
import random

# initialize pygame
pygame.init()

# nastavení obrazovky
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Star Keeper')

# barvy
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 0)

# Hráč
player_width, player_height = 80, 20
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 50
player_speed = 7

# Hvězdy
star_width, star_height = 20, 20
stars = []
star_speed = 5
spawn_rate = 30  # vyšší číslo = méně hvězd
frame_count = 0

# skóre
score = 0
# font
front = pygame.font.SysFont('arial', 24, bold=True)

# hlavní herní smyčka
running = True
while running:
    pygame.time.delay(30)
    screen.fill(BLUE)

    # události
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # pohyb hráče
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # generování hvězd
    frame_count += 1
    if frame_count >= spawn_rate:
        star_x = random.randint(0, WIDTH - star_width)
        stars.append([star_x, -star_height])
        frame_count = 0

    # pohyb hvězd a kontrola kolizí
    for star in stars:
        star[1] += star_speed
        if star[1] + star_height >= player_y and player_x < star[0] + star_width and player_x + player_width > star[0]:
            score += 1
            stars.remove(star)
        elif star[1] > HEIGHT:
            stars.remove(star)

    # vykreslení hráče a hvězd
    pygame.draw.rect(screen, WHITE, (player_x, player_y, player_width, player_height))
    for star in stars:
        pygame.draw.circle(screen, YELLOW, (star[0] + star_width // 2, star[1] + star_height // 2), star_width // 2)

    # zobrazit skóre
    score_text = front.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

=======
import pygame
import random

# initialize pygame
pygame.init()

# nastavení obrazovky
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Star Keeper')

# barvy
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 0)

# Hráč
player_width, player_height = 80, 20
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 50
player_speed = 7

# Hvězdy
star_width, star_height = 20, 20
stars = []
star_speed = 5
spawn_rate = 30  # vyšší číslo = méně hvězd
frame_count = 0

# skóre
score = 0
# font
front = pygame.font.SysFont('arial', 24, bold=True)

# hlavní herní smyčka
running = True
while running:
    pygame.time.delay(30)
    screen.fill(BLUE)

    # události
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # pohyb hráče
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # generování hvězd
    frame_count += 1
    if frame_count >= spawn_rate:
        star_x = random.randint(0, WIDTH - star_width)
        stars.append([star_x, -star_height])
        frame_count = 0

    # pohyb hvězd a kontrola kolizí
    for star in stars:
        star[1] += star_speed
        if star[1] + star_height >= player_y and player_x < star[0] + star_width and player_x + player_width > star[0]:
            score += 1
            stars.remove(star)
        elif star[1] > HEIGHT:
            stars.remove(star)

    # vykreslení hráče a hvězd
    pygame.draw.rect(screen, WHITE, (player_x, player_y, player_width, player_height))
    for star in stars:
        pygame.draw.circle(screen, YELLOW, (star[0] + star_width // 2, star[1] + star_height // 2), star_width // 2)

    # zobrazit skóre
    score_text = front.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

>>>>>>> 9e7ab7b3ef6df452d38f6e299e8638294bc4098e
pygame.quit()