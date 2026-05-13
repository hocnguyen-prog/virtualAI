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
ai_network = None  # Store trained AI network

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
        f.write("""[NEAT]
fitness_criterion = max
fitness_threshold = 100
pop_size = 50
reset_on_extinction = False
no_fitness_termination = False

[DefaultGenome]
activation_default = tanh
activation_mutate_rate = 0.0
activation_options = tanh
aggregation_default = sum
aggregation_mutate_rate = 0.0
aggregation_options = sum
bias_attr_mutation_type = gaussian
bias_init_mean = 0.0
bias_init_stdev = 1.0
bias_max_value = 30.0
bias_min_value = -30.0
bias_mutate_power = 0.5
bias_mutate_rate = 0.7
bias_replace_rate = 0.1
compatibility_threshold = 3.0
conn_add_prob = 0.5
conn_delete_prob = 0.2
feed_forward = True
initial_connection = full
node_add_prob = 0.2
node_delete_prob = 0.2
num_hidden = 0
num_inputs = 3
num_outputs = 1
response_init_mean = 1.0
response_init_stdev = 0.0
response_max_value = 30.0
response_min_value = -30.0
response_mutate_power = 0.0
response_mutate_rate = 0.0
response_replace_rate = 0.0
weight_attr_mutation_type = gaussian
weight_init_mean = 0.0
weight_init_stdev = 1.0
weight_max_value = 30
weight_min_value = -30
weight_mutate_power = 0.5
weight_mutate_rate = 0.8
weight_replace_rate = 0.1

[DefaultSpeciesSet]
compatibility_threshold = 3.0

[DefaultStagnation]
species_fitness_func = max
max_stagnation = 20
species_elitism = 2

[DefaultReproduction]
elitism = 2
survival_threshold = 0.2
min_species_size = 2
reset_on_extinction = False
""")

def run_ai():
    global ai_network
    
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        "neat_config.txt"
    )

    p = neat.Population(config)
    
    winner = p.run(eval_genomes, 20)
    
    # Save the best network
    ai_network = neat.nn.FeedForwardNetwork.create(winner, config)
    print(f"AI training complete! Best fitness: {winner.fitness}")


def eval_genomes(genomes, config):
    nets = []
    birds = []
    ge = []
    ge_map = {}
    pipes = [Pipe()]
    alive = set()

    for idx, (_, g) in enumerate(genomes):
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird())
        g.fitness = 0.0
        ge.append(g)
        alive.add(idx)
        ge_map[idx] = g

    frames = 0
    while len(alive) > 0 and frames < 3000:
        frames += 1
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if len(pipes) == 0 or pipes[-1].x < 200:
            pipes.append(Pipe())

        for idx in list(alive):
            bird = birds[idx]
            bird.move()
            ge_map[idx].fitness += 0.1

            # Find closest pipe
            pipe = None
            for p in pipes:
                if p.x + 80 > bird.x:
                    pipe = p
                    break
            
            if pipe is None:
                pipe = pipes[0] if pipes else Pipe()

            # Better inputs: bird y, pipe center height, distance to pipe
            gap_center = (pipe.h + pipe.gap / 2) / HEIGHT
            inputs = (bird.y / HEIGHT, gap_center, (pipe.x - bird.x) / WIDTH)
            output = nets[idx].activate(inputs)

            if output[0] > 0.5:
                bird.jump()

            # Collision detection
            if (bird.x + 20 > pipe.x and bird.x - 20 < pipe.x + 80 and
                (bird.y - 20 < pipe.h or bird.y + 20 > pipe.h + pipe.gap)):
                alive.discard(idx)
                ge_map[idx].fitness -= 1.0

            if bird.y < 0 or bird.y > HEIGHT:
                alive.discard(idx)

        for p in pipes:
            p.move()

        # Remove off-screen pipes and reward
        if pipes[0].x < -80:
            pipes.pop(0)
            for idx in alive:
                ge_map[idx].fitness += 10.0

        screen.fill((135,206,235))
        for p in pipes:
            p.draw()
        for idx in alive:
            birds[idx].draw()
        pygame.display.update()


# shop menu
def shop_menu():
    global coins, current_skin, owned_skins

    running = True
    while running:
        screen.fill((30,30,30))
        
        title = font.render("SHOP", True, (255,255,255))
        screen.blit(title, (250, 50))
        
        coins_txt = font.render(f"Coins: {coins}", True, (255,215,0))
        screen.blit(coins_txt, (250, 100))

        y = 150
        for skin, price in skins.items():
            status = "OWNED" if skin in owned_skins else f"{price} coins"
            color = (100, 255, 100) if skin in owned_skins else (255, 200, 0)
            txt = font.render(f"{skin.upper()} - {status}", True, color)
            screen.blit(txt, (150, y))
            
            pygame.draw.rect(screen, color, (120, y-5, 360, 40), 2)
            y += 70
        
        back_txt = font.render("ESC = back", True, (200,200,200))
        screen.blit(back_txt, (200, 700))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                y = 150
                for skin, price in skins.items():
                    rect = pygame.Rect(120, y-5, 360, 40)

                    if rect.collidepoint(mx, my):
                        if skin in owned_skins:
                            current_skin = skin
                        elif coins >= price:
                            coins -= price
                            owned_skins.append(skin)
                            current_skin = skin

                    y += 70


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

    game_state = "menu"
    score = 0
    bird = Bird()
    pipes = [Pipe()]
    running = True

    while running:
        clock.tick(60)
        screen.fill((135,206,235))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if game_state == "menu":
                    if event.key == pygame.K_SPACE:
                        game_state = "play"
                    elif event.key == pygame.K_s:
                        shop_menu()
                    elif event.key == pygame.K_a:
                        ai_mode = not ai_mode
                    elif event.key == pygame.K_n:
                        run_ai()

                elif game_state == "play":
                    if event.key == pygame.K_SPACE and not ai_mode:
                        bird.jump()

                elif game_state == "gameover":
                    if event.key == pygame.K_r:
                        game_state = "menu"
                        score = 0
                        bird = Bird()
                        pipes = [Pipe()]

        if game_state == "menu":
            screen.blit(font.render("Flappy ULTRA", True, (0,0,0)), (200,200))
            screen.blit(font.render("SPACE = play", True, (0,0,0)), (200,250))
            screen.blit(font.render("S = shop", True, (0,0,0)), (200,300))
            screen.blit(font.render("A = toggle AI", True, (0,0,0)), (200,350))
            screen.blit(font.render("N = train AI", True, (0,0,0)), (200,400))
            screen.blit(font.render(f"AI: {'ON' if ai_mode else 'OFF'}", True, (100,255,100) if ai_mode else (255,0,0)), (200,450))

        elif game_state == "play":
            bird.move()

            for p in pipes:
                p.move()

            if pipes[0].x < -80:
                pipes.pop(0)
                pipes.append(Pipe())
                score += 1
                coins += 1

            # Find next pipe
            next_pipe = None
            for p in pipes:
                if p.x + 80 > bird.x:
                    next_pipe = p
                    break
            if next_pipe is None:
                next_pipe = pipes[0]

            # AI mode: use trained network
            if ai_mode and ai_network is not None:
                gap_center = (next_pipe.h + next_pipe.gap / 2) / HEIGHT
                ai_input = (bird.y / HEIGHT, gap_center, (next_pipe.x - bird.x) / WIDTH)
                ai_output = ai_network.activate(ai_input)
                if ai_output[0] > 0.5:
                    bird.jump()

            # Collision detection
            for p in pipes:
                if (bird.x + 20 > p.x and bird.x - 20 < p.x + 80 and
                    (bird.y - 20 < p.h or bird.y + 20 > p.h + p.gap)):
                    game_state = "gameover"
                    send_score(score)

            if bird.y < 0 or bird.y > HEIGHT:
                game_state = "gameover"

            bird.draw()
            for p in pipes:
                p.draw()

            screen.blit(font.render(f"Score: {score}", True, (0,0,0)), (10,10))
            if ai_mode:
                screen.blit(font.render("AI Mode: ON", True, (100,255,100)), (10,50))

        elif game_state == "gameover":
            high_score = max(high_score, score)
            screen.blit(font.render("Game Over", True, (255,0,0)), (200,200))
            screen.blit(font.render(f"Score: {score}", True, (0,0,0)), (200,250))
            screen.blit(font.render(f"High: {high_score}", True, (0,0,0)), (200,300))
            screen.blit(font.render("R = restart", True, (0,0,0)), (200,350))

        pygame.display.flip()


if __name__ == "__main__":
    create_config()
    try:
        main()
    except KeyboardInterrupt:
        pygame.quit()
        print("Game closed")