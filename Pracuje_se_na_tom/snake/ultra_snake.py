import pygame
import random
import math
import sys
import array

# --- KONFIGURACE ---
SIRKA, VYSKA = 800, 600
POLE = 40  
FPS = 10

# Google Paleta barev
ZELENA_SVETLA = (170, 215, 81)
ZELENA_TMAVA = (162, 209, 73)
MODRA_HLAVA = (78, 124, 246)
MODRA_TELO = (92, 136, 253)
CERVENA_JABLKO = (231, 71, 29)

class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=1)
        self.dis = pygame.display.set_mode((SIRKA, VYSKA))
        pygame.display.set_caption('Google Snake Ultra Edition')
        self.clock = pygame.time.Clock()
        self.font_skore = pygame.font.SysFont("arial", 30, bold=True)
        self.font_menu = pygame.font.SysFont("arial", 50, bold=True)
        self.castice = []
        self.reset()
        self.v_menu = True

    def reset(self):
        # Startovní pozice: hlava a dva články těla
        self.had = [[4*POLE, 5*POLE], [3*POLE, 5*POLE], [2*POLE, 5*POLE]]
        self.smer = "RIGHT"
        self.dalsi_smer = "RIGHT"
        self.jidlo = self.nove_jidlo()
        self.skore = 0
        self.rychlost = FPS

    def nove_jidlo(self):
        while True:
            x = random.randrange(0, SIRKA, POLE)
            y = random.randrange(0, VYSKA, POLE)
            if [x, y] not in self.had: return [x, y]

    def hrej_zvuk(self, typ):
        """Generuje zvukové pípnutí přímo v paměti (opraveno pro Python 3.13)"""
        freq = 480 if typ == "jidlo" else 180
        duration = 0.1
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        
        # 'h' znamená signed short (16-bit), což vyřeší tvou chybu ValueError
        buf = array.array('h', [
            int(16383 * math.sin(2 * math.pi * freq * i / sample_rate)) 
            for i in range(n_samples)
        ])
        
        try:
            sound = pygame.mixer.Sound(buffer=buf)
            sound.set_volume(0.1)
            sound.play()
        except:
            pass # Pokud by byl problém s audio zařízením, hra nespadne

    def efekt_jidla(self, x, y):
        """Vytvoří efekt rozprsknutí při snězení jablka"""
        for _ in range(15):
            self.castice.append({
                "x": x + POLE//2, "y": y + POLE//2,
                "dx": random.uniform(-6, 6), "dy": random.uniform(-6, 6),
                "life": 1.0
            })

    def kresli_sachovnici(self):
        for y in range(0, VYSKA, POLE):
            for x in range(0, SIRKA, POLE):
                barva = ZELENA_SVETLA if (x // POLE + y // POLE) % 2 == 0 else ZELENA_TMAVA
                pygame.draw.rect(self.dis, barva, [x, y, POLE, POLE])

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.v_menu and event.key == pygame.K_SPACE:
                    self.v_menu = False
                if event.key == pygame.K_UP and self.smer != "DOWN": self.dalsi_smer = "UP"
                elif event.key == pygame.K_DOWN and self.smer != "UP": self.dalsi_smer = "DOWN"
                elif event.key == pygame.K_LEFT and self.smer != "RIGHT": self.dalsi_smer = "LEFT"
                elif event.key == pygame.K_RIGHT and self.smer != "LEFT": self.dalsi_smer = "RIGHT"

        if self.v_menu: return

        self.smer = self.dalsi_smer
        hlava = list(self.had[0])

        if self.smer == "UP": hlava[1] -= POLE
        elif self.smer == "DOWN": hlava[1] += POLE
        elif self.smer == "LEFT": hlava[0] -= POLE
        elif self.smer == "RIGHT": hlava[0] += POLE

        # Kontrola kolize se zdí nebo tělem
        if (hlava[0] < 0 or hlava[0] >= SIRKA or 
            hlava[1] < 0 or hlava[1] >= VYSKA or 
            hlava in self.had):
            self.hrej_zvuk("prohra")
            self.v_menu = True
            self.reset()
            return

        self.had.insert(0, hlava)
        
        # Snězení jídla
        if hlava == self.jidlo:
            self.skore += 1
            self.hrej_zvuk("jidlo")
            self.efekt_jidla(hlava[0], hlava[1])
            self.jidlo = self.nove_jidlo()
            self.rychlost = FPS + (self.skore // 2)
        else:
            self.had.pop()

    def vykresli(self):
        if self.v_menu:
            self.dis.fill(ZELENA_SVETLA)
            t1 = self.font_menu.render("SNAKE ULTRA", True, (255, 255, 255))
            t2 = self.font_skore.render("Stiskni MEZERNÍK pro start", True, (0, 0, 0))
            self.dis.blit(t1, (SIRKA//2 - t1.get_width()//2, VYSKA//3))
            self.dis.blit(t2, (SIRKA//2 - t2.get_width()//2, VYSKA//2))
            pygame.display.update()
            return

        self.kresli_sachovnici()

        # Animace částic
        for p in self.castice[:]:
            p["x"] += p["dx"]; p["y"] += p["dy"]; p["life"] -= 0.08
            if p["life"] <= 0: self.castice.remove(p)
            else:
                alpha = int(p["life"] * 255)
                pygame.draw.circle(self.dis, CERVENA_JABLKO, (int(p["x"]), int(p["y"])), 4)

        # Jablko
        jx, jy = self.jidlo
        pygame.draw.circle(self.dis, CERVENA_JABLKO, (jx + POLE//2, jy + POLE//2), POLE//2 - 4)
        pygame.draw.rect(self.dis, (100, 50, 0), [jx + POLE//2 - 2, jy + 4, 4, 8])

        # Had
        for i, (hx, hy) in enumerate(self.had):
            barva = MODRA_HLAVA if i == 0 else MODRA_TELO
            pygame.draw.rect(self.dis, barva, [hx + 2, hy + 2, POLE - 4, POLE - 4], border_radius=10)
            
            if i == 0: # Oči hlavy
                self.kresli_oci(hx, hy)

        # Skóre
        skore_t = self.font_skore.render(f"🍎 {self.skore}", True, (255, 255, 255))
        self.dis.blit(skore_t, (20, 20))
        pygame.display.update()

    def kresli_oci(self, hx, hy):
        # Dynamické pozicování očí podle směru
        offset = 10
        if self.smer in ["RIGHT", "LEFT"]:
            o1 = (hx + POLE//2, hy + offset)
            o2 = (hx + POLE//2, hy + POLE - offset)
        else:
            o1 = (hx + offset, hy + POLE//2)
            o2 = (hx + POLE - offset, hy + POLE//2)
        
        pygame.draw.circle(self.dis, (255, 255, 255), o1, 6)
        pygame.draw.circle(self.dis, (255, 255, 255), o2, 6)
        pygame.draw.circle(self.dis, (0, 0, 0), o1, 3)
        pygame.draw.circle(self.dis, (0, 0, 0), o2, 3)

    def spustit(self):
        while True:
            self.update()
            self.vykresli()
            self.clock.tick(self.rychlost)

if __name__ == "__main__":
    SnakeGame().spustit()
