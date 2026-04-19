import pygame
import random
import math

# --- NASTAVENÍ ---
BLOCK_SIZE = 24
FPS = 60 # Vyšší FPS pro plynulý pohyb
SPEED = 2 # Rychlost v pixelech na snímek

MAZE_LAYOUT = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X............XX............X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "XOXXXX.XXXXX.XX.XXXXX.XXXXOX",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X..........................X",
    "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
    "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
    "X......XX....XX....XX......X",
    "XXXXXX.XXXXX XX XXXXX.XXXXXX",
    "     X.XXXXX XX XXXXX.X     ",
    "     X.XX    G     XX.X     ",
    "XXXXXX.XX XXX  XXX XX.XXXXXX",
    "      .   X G  G X   .      ", 
    "XXXXXX.XX XXXXXXXX XX.XXXXXX",
    "     X.XX          XX.X     ",
    "     X.XX XXXXXXXX XX.X     ",
    "XXXXXX.XX XXXXXXXX XX.XXXXXX",
    "X............XX............X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "XO..XX.......P.......XX..OX",
    "XXX.XX.XX.XXXXXXXX.XX.XX.XXX",
    "XXX.XX.XX.XXXXXXXX.XX.XX.XXX",
    "X......XX....XX....XX......X",
    "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
    "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
    "X..........................X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

# Barvy
CLR_BG = (5, 5, 10)
CLR_WALL = (33, 33, 255)
CLR_PACMAN = (255, 255, 0)
CLR_GHOSTS = [(255, 0, 0), (255, 182, 193), (0, 255, 255), (255, 184, 82)]

class Entity:
    def __init__(self, x, y):
        self.pixel_x = x * BLOCK_SIZE
        self.pixel_y = y * BLOCK_SIZE
        self.vel_x = 0
        self.vel_y = 0

    def get_grid_pos(self):
        return self.pixel_x // BLOCK_SIZE, self.pixel_y // BLOCK_SIZE

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((len(MAZE_LAYOUT[0])*BLOCK_SIZE, len(MAZE_LAYOUT)*BLOCK_SIZE + 50))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 18, bold=True)
        self.title_font = pygame.font.SysFont("Verdana", 40, bold=True)
        self.reset()

    def reset(self):
        self.maze = [list(row) for row in MAZE_LAYOUT]
        self.state = "START"
        self.score = 0
        self.lives = 3
        self.dots_total = sum(row.count('.') + row.count('O') for row in self.maze)
        self.dots_eaten = 0
        self.frame = 0
        
        # Najít startovní pozice
        ghost_counter = 0
        self.ghosts = []
        for r, row in enumerate(self.maze):
            for c, char in enumerate(row):
                if char == 'P':
                    self.pacman = Entity(c, r)
                elif char == 'G':
                    g = Entity(c, r)
                    g.color = CLR_GHOSTS[ghost_counter % 4]
                    self.ghosts.append(g)
                    ghost_counter += 1

    def can_move(self, x, y, dx, dy):
        # Kontrola, zda je entita vycentrovaná v mřížce, aby mohla zatočit
        if x % BLOCK_SIZE == 0 and y % BLOCK_SIZE == 0:
            nx, ny = x // BLOCK_SIZE + dx, y // BLOCK_SIZE + dy
            if 0 <= nx < len(self.maze[0]) and 0 <= ny < len(self.maze):
                return self.maze[ny][nx] != 'X'
        return False

    def update(self):
        if self.state != "RUNNING":
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                if self.state in ["WIN", "OVER"]: self.reset()
                self.state = "RUNNING"
            return

        self.frame += 1
        keys = pygame.key.get_pressed()
        
        # Logika Pac-Mana
        if self.pacman.pixel_x % BLOCK_SIZE == 0 and self.pacman.pixel_y % BLOCK_SIZE == 0:
            if keys[pygame.K_UP] and self.can_move(self.pacman.pixel_x, self.pacman.pixel_y, 0, -1):
                self.pacman.vel_x, self.pacman.vel_y = 0, -SPEED
            elif keys[pygame.K_DOWN] and self.can_move(self.pacman.pixel_x, self.pacman.pixel_y, 0, 1):
                self.pacman.vel_x, self.pacman.vel_y = 0, SPEED
            elif keys[pygame.K_LEFT] and self.can_move(self.pacman.pixel_x, self.pacman.pixel_y, -1, 0):
                self.pacman.vel_x, self.pacman.vel_y = -SPEED, 0
            elif keys[pygame.K_RIGHT] and self.can_move(self.pacman.pixel_x, self.pacman.pixel_y, 1, 0):
                self.pacman.vel_x, self.pacman.vel_y = SPEED, 0
            
            # Zastavení o zeď
            if not self.can_move(self.pacman.pixel_x, self.pacman.pixel_y, 
                                1 if self.pacman.vel_x > 0 else -1 if self.pacman.vel_x < 0 else 0,
                                1 if self.pacman.vel_y > 0 else -1 if self.pacman.vel_y < 0 else 0):
                self.pacman.vel_x = self.pacman.vel_y = 0

        self.pacman.pixel_x += self.pacman.vel_x
        self.pacman.pixel_y += self.pacman.vel_y

        # Snězení tečky
        gx, gy = self.pacman.get_grid_pos()
        if self.maze[gy][gx] in ['.', 'O']:
            self.score += 10 if self.maze[gy][gx] == '.' else 50
            self.maze[gy][gx] = ' '
            self.dots_eaten += 1
            if self.dots_eaten >= self.dots_total: self.state = "WIN"

        # Duchové AI (jednoduchá, ale plynulá)
        for g in self.ghosts:
            if g.pixel_x % BLOCK_SIZE == 0 and g.pixel_y % BLOCK_SIZE == 0:
                dirs = [(SPEED,0), (-SPEED,0), (0,SPEED), (0,-SPEED)]
                valid_dirs = [d for d in dirs if self.can_move(g.pixel_x, g.pixel_y, d[0]//SPEED, d[1]//SPEED)]
                if valid_dirs:
                    g.vel_x, g.vel_y = random.choice(valid_dirs)
            g.pixel_x += g.vel_x
            g.pixel_y += g.vel_y
            
            # Kolize
            if abs(g.pixel_x - self.pacman.pixel_x) < 15 and abs(g.pixel_y - self.pacman.pixel_y) < 15:
                self.lives -= 1
                if self.lives <= 0: self.state = "OVER"
                else: 
                    self.pacman.pixel_x, self.pacman.pixel_y = 14*BLOCK_SIZE, 21*BLOCK_SIZE
                    self.pacman.vel_x = self.pacman.vel_y = 0

    def draw(self):
        self.screen.fill(CLR_BG)
        
        # Vykreslení bludiště
        for r, row in enumerate(self.maze):
            for c, char in enumerate(row):
                pos = (c*BLOCK_SIZE, r*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                if char == 'X':
                    pygame.draw.rect(self.screen, CLR_WALL, (c*BLOCK_SIZE+3, r*BLOCK_SIZE+3, BLOCK_SIZE-6, BLOCK_SIZE-6), 2, 4)
                elif char == '.':
                    pygame.draw.circle(self.screen, (255,200,150), (c*BLOCK_SIZE+BLOCK_SIZE//2, r*BLOCK_SIZE+BLOCK_SIZE//2), 2)
                elif char == 'O':
                    if self.frame % 20 < 10:
                        pygame.draw.circle(self.screen, (255,255,255), (c*BLOCK_SIZE+BLOCK_SIZE//2, r*BLOCK_SIZE+BLOCK_SIZE//2), 5)

        # Pacman s animací pusy
        p_center = (self.pacman.pixel_x + BLOCK_SIZE//2, self.pacman.pixel_y + BLOCK_SIZE//2)
        mouth = abs(math.sin(self.frame * 0.2)) * 30
        pygame.draw.circle(self.screen, CLR_PACMAN, p_center, BLOCK_SIZE//2 - 2)
        
        # "Vykousnutí" pusy (černý trojúhelník)
        angle = 0
        if self.pacman.vel_x < 0: angle = 180
        elif self.pacman.vel_y < 0: angle = 90
        elif self.pacman.vel_y > 0: angle = 270
        
        p1 = p_center
        p2 = (p_center[0] + 15 * math.cos(math.radians(angle - mouth)), p_center[1] - 15 * math.sin(math.radians(angle - mouth)))
        p3 = (p_center[0] + 15 * math.cos(math.radians(angle + mouth)), p_center[1] - 15 * math.sin(math.radians(angle + mouth)))
        pygame.draw.polygon(self.screen, CLR_BG, [p1, p2, p3])

        # Duchové s vlnkami
        for g in self.ghosts:
            gx, gy = g.pixel_x + 2, g.pixel_y + 2
            pygame.draw.ellipse(self.screen, g.color, (gx, gy, BLOCK_SIZE-4, BLOCK_SIZE-4))
            pygame.draw.rect(self.screen, g.color, (gx, gy + BLOCK_SIZE//2 - 2, BLOCK_SIZE-4, BLOCK_SIZE//2))
            # Oči
            pygame.draw.circle(self.screen, (255,255,255), (gx+6, gy+8), 3)
            pygame.draw.circle(self.screen, (255,255,255), (gx+14, gy+8), 3)

        # UI
        score_surf = self.font.render(f"SCORE: {self.score}   LIVES: {'♥'*self.lives}", True, (255,255,255))
        self.screen.blit(score_surf, (15, self.screen.get_height() - 35))

        # Tabulka po vyhrání
        if self.state == "WIN":
            self.draw_end_screen("LEVEL CLEAR!", (0, 255, 100))
        elif self.state == "OVER":
            self.draw_end_screen("GAME OVER", (255, 50, 50))
        elif self.state == "START":
            self.draw_end_screen("READY?", CLR_PACMAN, "PRESS SPACE")

        pygame.display.flip()

    def draw_end_screen(self, msg, color, submsg="SPACE TO RESTART"):
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0,0))
        
        m_surf = self.title_font.render(msg, True, color)
        s_surf = self.font.render(f"FINAL SCORE: {self.score}", True, (255,255,255))
        r_surf = self.font.render(submsg, True, (200,200,200))
        
        self.screen.blit(m_surf, (self.screen.get_width()//2 - m_surf.get_width()//2, 200))
        self.screen.blit(s_surf, (self.screen.get_width()//2 - s_surf.get_width()//2, 260))
        self.screen.blit(r_surf, (self.screen.get_width()//2 - r_surf.get_width()//2, 320))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    Game().run()