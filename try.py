import tkinter as tk
from tkinter import messagebox

class PiskvorkyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Piškvorky 5x5")
        
        self.hrac = "X"
        self.buttons = [[None for _ in range(5)] for _ in range(5)]
        self.plocha = [["" for _ in range(5)] for _ in range(5)]
        
        # Vytvoření tlačítek
        for r in range(5):
            for c in range(5):
                self.buttons[r][c] = tk.Button(root, text="", font=('Arial', 20), width=5, height=2,
                                               command=lambda r=r, c=c: self.kliknuti(r, c))
                self.buttons[r][c].grid(row=r, column=c)

    def kliknuti(self, r, c):
        if self.plocha[r][c] == "":
            self.plocha[r][c] = self.hrac
            self.buttons[r][c].config(text=self.hrac)
            
            if self.zkontroluj_vitezstvi(r, c):
                messagebox.showinfo("Konec hry", f"Vyhrál hráč {self.hrac}!")
                self.reset_hry()
            elif self.je_remiza():
                messagebox.showinfo("Konec hry", "Remíza!")
                self.reset_hry()
            else:
                self.hrac = "O" if self.hrac == "X" else "X"

    def zkontroluj_vitezstvi(self, r, c):
        # Kontrola řádku, sloupce a obou diagonál
        smery = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in smery:
            count = 1
            # Zpětný směr
            i = 1
            while 0 <= r - i*dr < 5 and 0 <= c - i*dc < 5 and self.plocha[r - i*dr][c - i*dc] == self.hrac:
                count += 1
                i += 1
            # Dopředný směr
            i = 1
            while 0 <= r + i*dr < 5 and 0 <= c + i*dc < 5 and self.plocha[r + i*dr][c + i*dc] == self.hrac:
                count += 1
                i += 1
            if count >= 5:
                return True
        return False

    def je_remiza(self):
        return all(all(cell != "" for cell in row) for row in self.plocha)

    def reset_hry(self):
        self.plocha = [["" for _ in range(5)] for _ in range(5)]
        self.hrac = "X"
        for r in range(5):
            for c in range(5):
                self.buttons[r][c].config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = PiskvorkyApp(root)
    root.mainloop()