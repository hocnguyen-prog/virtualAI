import pygame
import neat
import random
import requests
import os

pygame.init()

WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy ULTRA")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28)

# game data
coins = 0
score = 0
high_score = 0

skins = {"red": 50, "blue": 100}
owned_skins = ["yellow"]
current_skin = "yellow"

game_state = "menu"  # menu, play, shop, gameover
ai_mode = False

# bird
class Bird:
    def __init__(self, x=100):
        self.x = x
        self.y = 300
        self.vel = 0

    def jump(self):
        self.vel = -10

    def move(self):
        self.vel += 0.5
        self.y += self.vel

    def draw(self):
        color = (255,230,0)
        if current_skin == "red":
            color = (255,0,0)
        elif current_skin == "blue":
            color = (0,0,255)

        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 20)


# pipe
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.h = random.randint(100, 500)
        self.gap = 150
        self.passed = False

    def move(self):
        self.x -= 5

    def draw(self):
        pygame.draw.rect(screen, (0,200,0), (self.x, 0, 80, self.h))
        pygame.draw.rect(screen, (0,200,0), (self.x, self.h+self.gap, 80, HEIGHT))


# neat setup
def create_config():
    with open("neat_config.txt", "w") as f:
        f.write("""
[NEAT]
fitness_criterion = max
fitness_threshold = 50
pop_size = 30

[DefaultGenome]
num_inputs = 2
num_outputs = 1
num_hidden = 0

activation_default = tanh

[DefaultSpeciesSet]
compatibility_threshold = 3.0
""")

def run_ai():
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        "neat_config.txt"
    )

    p = neat.Population(config)
    p.run(eval_genomes, 10)


def eval_genomes(genomes, config):
    nets = []
    birds = []
    ge = []
    pipes = [Pipe()]

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird())
        g.fitness = 0
        ge.append(g)

    run = True
    while run and len(birds) > 0:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pipe = pipes[0]

        for i, bird in enumerate(birds):
            bird.move()
            ge[i].fitness += 0.1

            inputs = (bird.y, abs(bird.y - pipe.h))
            output = nets[i].activate(inputs)

            if output[0] > 0.5:
                bird.jump()

        for p in pipes:
            p.move()

        if pipes[0].x < -80:
            pipes.pop(0)
            pipes.append(Pipe())

        for i, bird in enumerate(birds):
            if bird.y < 0 or bird.y > HEIGHT:
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)

        screen.fill((135,206,235))
        for p in pipes:
            p.draw()
        for bird in birds:
            bird.draw()
        pygame.display.update()


# shop menu
def shop_menu():
    global coins

    running = True
    while running:
        screen.fill((30,30,30))

        y = 150
        for skin, price in skins.items():
            txt = font.render(f"{skin} - {price}", True, (255,255,255))
            rect = txt.get_rect(topleft=(200,y))
            screen.blit(txt, rect)

            pygame.draw.rect(screen, (255,255,255), rect, 2)
            y += 60

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                y = 150
                for skin, price in skins.items():
                    rect = pygame.Rect(200,y,200,40)

                    if rect.collidepoint(mx, my):
                        if coins >= price and skin not in owned_skins:
                            coins -= price
                            owned_skins.append(skin)

                    y += 60


# leaderboard
def send_score(score):
    try:
        requests.post("http://127.0.0.1:5000/score",
                      json={"name":"player","score":score})
    except:
        pass


# main game loop
def main():
    global score, game_state, coins, high_score, ai_mode

    bird = Bird()
    pipes = [Pipe()]

    while True:
        clock.tick(60)
        screen.fill((135,206,235))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if game_state == "menu":
                    if event.key == pygame.K_SPACE:
                        game_state = "play"
                    if event.key == pygame.K_s:
                        shop_menu()
                    if event.key == pygame.K_a:
                        ai_mode = not ai_mode
                    if event.key == pygame.K_n:
                        run_ai()

                elif game_state == "play":
                    if event.key == pygame.K_SPACE:
                        bird.jump()

                elif game_state == "gameover":
                    if event.key == pygame.K_r:
                        main()

        if game_state == "menu":
            screen.blit(font.render("Flappy ULTRA", True, (0,0,0)), (200,200))
            screen.blit(font.render("SPACE = play", True, (0,0,0)), (200,250))
            screen.blit(font.render("S = shop", True, (0,0,0)), (200,300))
            screen.blit(font.render("A = toggle AI", True, (0,0,0)), (200,350))
            screen.blit(font.render("N = train AI", True, (0,0,0)), (200,400))

        elif game_state == "play":
            bird.move()

            for p in pipes:
                p.move()

            if pipes[0].x < -80:
                pipes.pop(0)
                pipes.append(Pipe())
                score += 1
                coins += 1

            for p in pipes:
                if (bird.x > p.x and bird.x < p.x+80 and
                    (bird.y < p.h or bird.y > p.h+p.gap)):
                    game_state = "gameover"
                    send_score(score)

            if bird.y < 0 or bird.y > HEIGHT:
                game_state = "gameover"

            bird.draw()
            for p in pipes:
                p.draw()

            screen.blit(font.render(f"Score: {score}", True, (0,0,0)), (10,10))

        elif game_state == "gameover":
            high_score = max(high_score, score)
            screen.blit(font.render("Game Over", True, (255,0,0)), (200,200))
            screen.blit(font.render(f"Score: {score}", True, (0,0,0)), (200,250))
            screen.blit(font.render(f"High: {high_score}", True, (0,0,0)), (200,300))
            screen.blit(font.render("R = restart", True, (0,0,0)), (200,350))

        pygame.display.flip()


create_config()
main()