import pygame
import random

# --- KONFIGURACE ---
SIZE = 25  # Velikost jednoho čtverce
FPS = 8    # Pomalejší rychlost, aby se to dalo hrát i bez plynulého pohybu

MAZE = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X............XX............X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X.X  X.X   X.XX.X   X.X  X.X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X..........................X",
    "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
    "X......XX....XX....XX......X",
    "XXXXXX.XXXXX XX XXXXX.XXXXXX",
    "     X.XX          XX.X     ",
    "XXXXXX.XX XXXXXXXX XX.XXXXXX",
    "X............XX............X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X...XX.......P.......XX...OX",
    "XXX.XX.XX.XXXXXXXX.XX.XX.XXX",
    "X......XX....XX....XX......X",
    "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
    "X..........................X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

# Barvy
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE   = (0, 0, 255)
RED    = (255, 0, 0)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((len(MAZE[0])*SIZE, len(MAZE)*SIZE + 50))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        self.reset()

    def reset(self):
        self.map = [list(row) for row in MAZE]
        self.score = 0
        self.lives = 3
        self.state = "PLAY" # PLAY, WIN, DEAD
        
        # Najít startovní pozici Pacmana
        for r in range(len(self.map)):
            for c in range(len(self.map[r])):
                if self.map[r][c] == 'P':
                    self.pac_x, self.pac_y = c, r
        
        # Duchové (jednoduché seznamy místo tříd)
        self.ghosts = [[1, 1], [26, 1], [1, 17]] 

    def move_player(self, dx, dy):
        # Kontrola, jestli tam není zeď
        new_x = self.pac_x + dx
        new_y = self.pac_y + dy
        
        if self.map[new_y][new_x] != 'X':
            self.pac_x, self.pac_y = new_x, new_y
            
            # Snězení tečky
            if self.map[self.pac_y][self.pac_x] == '.':
                self.map[self.pac_y][self.pac_x] = ' '
                self.score += 10
            elif self.map[self.pac_y][self.pac_x] == 'O':
                self.map[self.pac_y][self.pac_x] = ' '
                self.score += 50

    def move_ghosts(self):
        for g in self.ghosts:
            # Náhodný pohyb: zkusí náhodný směr, pokud tam není zeď
            dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(dirs)
            for dx, dy in dirs:
                if self.map[g[1]+dy][g[0]+dx] != 'X':
                    g[0] += dx
                    g[1] += dy
                    break

    def check_collisions(self):
        for g in self.ghosts:
            if g[0] == self.pac_x and g[1] == self.pac_y:
                self.lives -= 1
                self.pac_x, self.pac_y = 14, 13 # Restart pozice
                if self.lives <= 0:
                    self.state = "DEAD"

    def draw(self):
        self.screen.fill(BLACK)
        
        # 1. Vykreslení mapy
        for r in range(len(self.map)):
            for c in range(len(self.map[r])):
                char = self.map[r][c]
                px, py = c * SIZE, r * SIZE
                
                if char == 'X':
                    pygame.draw.rect(self.screen, BLUE, (px+1, py+1, SIZE-2, SIZE-2), 1)
                elif char == '.':
                    pygame.draw.circle(self.screen, WHITE, (px+SIZE//2, py+SIZE//2), 2)
                elif char == 'O':
                    pygame.draw.circle(self.screen, WHITE, (px+SIZE//2, py+SIZE//2), 5)

        # 2. Vykreslení Pacmana
        pygame.draw.circle(self.screen, YELLOW, (self.pac_x*SIZE + SIZE//2, self.pac_y*SIZE + SIZE//2), SIZE//2 - 2)

        # 3. Vykreslení duchů
        for g in self.ghosts:
            pygame.draw.rect(self.screen, RED, (g[0]*SIZE+4, g[1]*SIZE+4, SIZE-8, SIZE-8))

        # 4. Texty a tabulka
        score_text = self.font.render(f"Skóre: {self.score}  Životy: {self.lives}", True, WHITE)
        self.screen.blit(score_text, (10, len(self.map)*SIZE + 10))

        if self.state != "PLAY":
            # Tabulka výsledků
            overlay = pygame.Surface((300, 150))
            overlay.fill((50, 50, 50))
            self.screen.blit(overlay, (100, 150))
            
            res_msg = "VYHRÁL JSI!" if self.state == "WIN" else "KONEC HRY"
            msg = self.font.render(res_msg, True, YELLOW)
            pts = self.font.render(f"Celkem bodů: {self.score}", True, WHITE)
            restart = self.font.render("Stiskni R pro restart", True, WHITE)
            
            self.screen.blit(msg, (150, 170))
            self.screen.blit(pts, (150, 200))
            self.screen.blit(restart, (150, 240))

        pygame.display.flip()

    def run(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            if self.state == "PLAY":
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:  self.move_player(-1, 0)
                if keys[pygame.K_RIGHT]: self.move_player(1, 0)
                if keys[pygame.K_UP]:    self.move_player(0, -1)
                if keys[pygame.K_DOWN]:  self.move_player(0, 1)
                
                self.move_ghosts()
                self.check_collisions()
                
                # Kontrola výhry (žádné tečky)
                dots = sum(row.count('.') for row in self.map)
                if dots == 0: self.state = "WIN"
            else:
                if pygame.key.get_pressed()[pygame.K_r]:
                    self.reset()

            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    Game().run()