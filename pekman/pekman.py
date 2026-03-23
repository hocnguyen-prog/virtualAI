"""
PEKMAN - Pac-Man hra v Pythonu
Ovládání: Šipky (nahoru, dolů, doleva, doprava)
Cíl: Sebrat všechny pelétky a vyhnout se duchům
"""

import pygame
import random
import sys
from enum import Enum

# Inicializace Pygame
pygame.init()

# Konstanty
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GAME_SPEED = 5

# Barvy
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Směry
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    NONE = (0, 0)


class Pacman:
    """Třída pro Pac-Mana"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = Direction.NONE
        self.next_direction = Direction.NONE
        self.mouth_open = True
        self.frame = 0
        
    def update(self, walls):
        """Aktualizuje pozici Pac-Mana"""
        # Pokus se jít požadovaným směrem
        next_x = self.x + self.next_direction.value[0]
        next_y = self.y + self.next_direction.value[1]
        
        if self.is_valid_move(next_x, next_y, walls):
            self.direction = self.next_direction
            self.x = next_x
            self.y = next_y
        else:
            # Pokus se pokračovat v aktuálním směru
            next_x = self.x + self.direction.value[0]
            next_y = self.y + self.direction.value[1]
            if self.is_valid_move(next_x, next_y, walls):
                self.x = next_x
                self.y = next_y
        
        # Animace pusy
        self.frame += 1
        if self.frame % 10 == 0:
            self.mouth_open = not self.mouth_open
    
    def is_valid_move(self, x, y, walls):
        """Kontroluje, zda je tah validní"""
        if x < 0 or x >= SCREEN_WIDTH // GRID_SIZE:
            return False
        if y < 0 or y >= SCREEN_HEIGHT // GRID_SIZE:
            return False
        return (x, y) not in walls
    
    def draw(self, screen):
        """Vykreslí Pac-Mana"""
        rect = pygame.Rect(
            self.x * GRID_SIZE + 2,
            self.y * GRID_SIZE + 2,
            GRID_SIZE - 4,
            GRID_SIZE - 4
        )
        pygame.draw.circle(
            screen, YELLOW,
            (rect.centerx, rect.centery),
            GRID_SIZE // 2 - 2
        )


class Ghost:
    """Třída pro duchy"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.direction = random.choice(list(Direction))
        self.direction = Direction.NONE if self.direction == Direction.NONE else self.direction
        
    def update(self, walls):
        """Aktualizuje pozici ducha"""
        # Random pohyb
        if random.random() < 0.03:
            self.direction = random.choice(
                [d for d in Direction if d != Direction.NONE]
            )
        
        next_x = self.x + self.direction.value[0]
        next_y = self.y + self.direction.value[1]
        
        # Pokud není validní, změň směr
        if not (0 <= next_x < SCREEN_WIDTH // GRID_SIZE and
                0 <= next_y < SCREEN_HEIGHT // GRID_SIZE and
                (next_x, next_y) not in walls):
            self.direction = random.choice(
                [d for d in Direction if d != Direction.NONE]
            )
        else:
            self.x = next_x
            self.y = next_y
    
    def draw(self, screen):
        """Vykreslí ducha"""
        rect = pygame.Rect(
            self.x * GRID_SIZE + 2,
            self.y * GRID_SIZE + 2,
            GRID_SIZE - 4,
            GRID_SIZE - 4
        )
        pygame.draw.rect(screen, self.color, rect)
        # Oči
        pygame.draw.circle(screen, WHITE, (rect.left + 5, rect.top + 5), 2)
        pygame.draw.circle(screen, WHITE, (rect.right - 5, rect.top + 5), 2)


class PacmanGame:
    """Hlavní třída hry"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("PEKMAN - Pac-Man Hra")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.reset_game()
        
    def reset_game(self):
        """Restartuje hru"""
        self.walls = self.create_maze()
        self.pacman = Pacman(1, 1)
        self.ghosts = [
            Ghost(5, 5, RED),
            Ghost(6, 5, PINK),
            Ghost(7, 5, CYAN),
            Ghost(8, 5, ORANGE),
        ]
        self.pellets = self.create_pellets()
        self.score = 0
        self.game_over = False
        self.won = False
        
    def create_maze(self):
        """Vytváří bludiště"""
        walls = set()
        
        # Hrany
        for x in range(40):
            walls.add((x, 0))
            walls.add((x, 29))
        
        for y in range(30):
            walls.add((0, y))
            walls.add((39, y))
        
        # Vnitřní zdi
        for x in range(5, 35):
            if x % 3 == 0:
                for y in range(5, 25):
                    if y % 4 == 0:
                        walls.add((x, y))
        
        return walls
    
    def create_pellets(self):
        """Vytváří pelétky"""
        pellets = set()
        for x in range(1, 39):
            for y in range(1, 29):
                if (x, y) not in self.walls and random.random() < 0.3:
                    pellets.add((x, y))
        return pellets
    
    def handle_input(self):
        """Zpracovává vstup"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.pacman.next_direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.pacman.next_direction = Direction.DOWN
                elif event.key == pygame.K_LEFT:
                    self.pacman.next_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.pacman.next_direction = Direction.RIGHT
                elif event.key == pygame.K_r:
                    self.reset_game()
        
        return True
    
    def update(self):
        """Aktualizuje stav hry"""
        if self.game_over or self.won:
            return
        
        self.pacman.update(self.walls)
        
        for ghost in self.ghosts:
            ghost.update(self.walls)
        
        # Sebírání peletek
        if (self.pacman.x, self.pacman.y) in self.pellets:
            self.pellets.remove((self.pacman.x, self.pacman.y))
            self.score += 10
        
        # Kontrola výhry
        if len(self.pellets) == 0:
            self.won = True
        
        # Kontrola kolize s duchy
        for ghost in self.ghosts:
            if self.pacman.x == ghost.x and self.pacman.y == ghost.y:
                self.game_over = True
    
    def draw(self):
        """Vykresluje hru"""
        self.screen.fill(BLACK)
        
        # Zdi
        for wall_x, wall_y in self.walls:
            pygame.draw.rect(
                self.screen, BLUE,
                (wall_x * GRID_SIZE, wall_y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            )
        
        # Pelétky
        for pellet_x, pellet_y in self.pellets:
            pygame.draw.circle(
                self.screen,
                WHITE,
                (pellet_x * GRID_SIZE + GRID_SIZE // 2,
                 pellet_y * GRID_SIZE + GRID_SIZE // 2),
                2
            )
        
        # Hráč a duchové
        self.pacman.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        
        # HUD
        score_text = self.font.render(f"Skore: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        pellets_left = self.small_font.render(
            f"Peletek: {len(self.pellets)}", True, WHITE
        )
        self.screen.blit(pellets_left, (10, 50))
        
        # Game Over / Won
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, RED)
            restart_text = self.small_font.render("Stiskni R pro restart", True, WHITE)
            self.screen.blit(
                game_over_text,
                (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 50)
            )
            self.screen.blit(
                restart_text,
                (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 20)
            )
        
        if self.won:
            won_text = self.font.render("VITEZSTVI!", True, YELLOW)
            restart_text = self.small_font.render("Stiskni R pro restart", True, WHITE)
            self.screen.blit(
                won_text,
                (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
            )
            self.screen.blit(
                restart_text,
                (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 20)
            )
        
        pygame.display.flip()
    
    def run(self):
        """Hlavní herní smyčka"""
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(GAME_SPEED)
        
        pygame.quit()
        sys.exit()


def main():
    """Spouští hru"""
    game = PacmanGame()
    game.run()


if __name__ == "__main__":
    main()
