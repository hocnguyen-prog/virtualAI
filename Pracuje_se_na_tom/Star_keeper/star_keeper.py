
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
SKIN = (255, 220, 180)
RED = (220, 50, 50)
BROWN = (139, 69, 19)

# Hráč (človíček s košíkem)
player_width, player_height = 60, 80
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 30
player_speed = 10

# Hvězdy
star_width, star_height = 20, 20
stars = []
star_speed = 3
spawn_rate = 30
frame_count = 0

# skóre
score = 0
game_over = False

# font
front = pygame.font.SysFont('arial', 24, bold=True)
game_over_font = pygame.font.SysFont('arial', 48, bold=True)

def draw_player(x, y):
    # nohy
    pygame.draw.rect(screen, (50, 50, 50), (x + 18, y + 55, 10, 25))
    pygame.draw.rect(screen, (50, 50, 50), (x + 32, y + 55, 10, 25))
    # tričko s vietnamskou vlajkou
    pygame.draw.rect(screen, (200, 30, 30), (x + 15, y + 25, 30, 30))  # červené tričko
    pygame.draw.circle(screen, (255, 255, 0), (x + 30, y + 40), 6)  # žlutá hvězda
    # hlava
    pygame.draw.circle(screen, SKIN, (x + 30, y + 12), 14)
    # ruce
    pygame.draw.rect(screen, SKIN, (x + 5, y + 30, 15, 8))
    pygame.draw.rect(screen, SKIN, (x + 40, y + 30, 15, 8))
    # košík (větší a viditelnější)
    pygame.draw.rect(screen, BROWN, (x + 10, y + 55, 40, 25))  # základ
    pygame.draw.rect(screen, BROWN, (x + 8, y + 50, 4, 15))    # levá stěna
    pygame.draw.rect(screen, BROWN, (x + 48, y + 50, 4, 15))   # pravá stěna
    pygame.draw.rect(screen, (160, 82, 45), (x + 12, y + 55, 36, 5))  # okraj

# hlavní herní smyčka
running = True
while running:
    pygame.time.delay(30)
    screen.fill(BLUE)

    # události
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                # restart hry
                score = 0
                game_over = False
                stars = []
                player_x = WIDTH // 2 - player_width // 2

    if not game_over:
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
        for star in stars[:]:
            star[1] += star_speed
            # kontrola zachycení (košík je dole)
            basket_y = player_y + 55
            if (star[1] + star_height >= basket_y and 
                player_x < star[0] + star_width and 
                player_x + player_width > star[0]):
                score += 1
                stars.remove(star)
            # game over - hvězda spadla na zem
            elif star[1] > HEIGHT:
                game_over = True

    # vykreslení hráče
    draw_player(player_x, player_y)

    # vykreslení hvězd
    for star in stars:
        pygame.draw.circle(screen, YELLOW, (star[0] + star_width // 2, star[1] + star_height // 2), star_width // 2)

    # zobrazit skóre
    score_text = front.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    # game over obrazovka
    if game_over:
        game_over_text = game_over_font.render('GAME OVER', True, RED)
        final_score_text = front.render(f'Final Score: {score}', True, WHITE)
        restart_text = front.render('Press R to restart', True, WHITE)
        
        screen.blit(game_over_text, (WIDTH//2 - 120, HEIGHT//2 - 50))
        screen.blit(final_score_text, (WIDTH//2 - 60, HEIGHT//2 + 10))
        screen.blit(restart_text, (WIDTH//2 - 80, HEIGHT//2 + 50))

    pygame.display.update()

pygame.quit()