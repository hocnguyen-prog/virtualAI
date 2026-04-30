import tkinter as tk
from tkinter import messagebox

class PiskvorkyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Piškvorky 20x20")
        self.root.configure(bg="#2c3e50")
        
        self.hrac = "X"
        self.velikost = 20  # 20x20 mřížka
        self.buttons = [[None for _ in range(self.velikost)] for _ in range(self.velikost)]
        self.plocha = [["" for _ in range(self.velikost)] for _ in range(self.velikost)]
        
        # Barvy pro hráče
        self.barva_x = "#e74c3c"   # Červená
        self.barva_o = "#3498db"   # Modrá
        self.barva_pozadi = "#34495e"
        
        # Nadpis
        tk.Label(root, text="PIŠKVORKY", font=('Arial', 24, 'bold'), 
                 bg="#2c3e50", fg="#ecf0f1").grid(row=0, column=0, columnspan=20, pady=10)
        
        # Info label
        self.info_label = tk.Label(root, text="Hraje: X", font=('Arial', 16, 'bold'),
                                   bg="#2c3e50", fg=self.barva_x)
        self.info_label.grid(row=1, column=0, columnspan=20, pady=5)
        
        # Vytvoření tlačítek - větší aréna
        for r in range(self.velikost):
            for c in range(self.velikost):
                self.buttons[r][c] = tk.Button(root, text="", font=('Arial', 12, 'bold'), 
                                               width=2, height=1, bg=self.barva_pozadi,
                                               fg="white", activebackground="#5d6d7e",
                                               command=lambda r=r, c=c: self.kliknuti(r, c))
                self.buttons[r][c].grid(row=r+2, column=c, padx=1, pady=1)

    def kliknuti(self, r, c):
        if self.plocha[r][c] == "":
            self.plocha[r][c] = self.hrac
            barva = self.barva_x if self.hrac == "X" else self.barva_o
            self.buttons[r][c].config(text=self.hrac, bg=barva)
            
            if self.zkontroluj_vitezstvi(r, c):
                messagebox.showinfo("Konec hry", f"Vyhrál hráč {self.hrac}! 🎉")
                self.reset_hry()
            elif self.je_remiza():
                messagebox.showinfo("Konec hry", "Remíza! 🤝")
                self.reset_hry()
            else:
                self.hrac = "O" if self.hrac == "X" else "X"
                barva = self.barva_x if self.hrac == "X" else self.barva_o
                self.info_label.config(text=f"Hraje: {self.hrac}", fg=barva)

    def zkontroluj_vitezstvi(self, r, c):
        # Kontrola řádku, sloupce a obou diagonál
        smery = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in smery:
            count = 1
            # Zpětný směr
            i = 1
            while 0 <= r - i*dr < self.velikost and 0 <= c - i*dc < self.velikost and self.plocha[r - i*dr][c - i*dc] == self.hrac:
                count += 1
                i += 1
            # Dopředný směr
            i = 1
            while 0 <= r + i*dr < self.velikost and 0 <= c + i*dc < self.velikost and self.plocha[r + i*dr][c + i*dc] == self.hrac:
                count += 1
                i += 1
            if count >= 5:
                return True
        return False

    def je_remiza(self):
        return all(all(cell != "" for cell in row) for row in self.plocha)

    def reset_hry(self):
        self.plocha = [["" for _ in range(self.velikost)] for _ in range(self.velikost)]
        self.hrac = "X"
        for r in range(self.velikost):
            for c in range(self.velikost):
                self.buttons[r][c].config(text="", bg=self.barva_pozadi)
        self.info_label.config(text="Hraje: X", fg=self.barva_x)

if __name__ == "__main__":
    root = tk.Tk()
    app = PiskvorkyApp(root)
    root.mainloop()