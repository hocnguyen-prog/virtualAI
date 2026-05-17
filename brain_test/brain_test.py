import random
import json
from pathlib import Path
import customtkinter as ctk
from typing import List, Dict


# ====================== DATA ======================
KNIHOVNA_OTAZEK: List[Dict] = [
    # === Klasické 4 možnosti ===
    {
        "otazka": "Na stromě sedí 5 ptáků. Lovec jednoho zastřelí. Kolik ptáků zůstalo?",
        "moznosti": ["4", "5", "0", "1"],
        "spravna": 2,
        "vysvetleni": "Ostatní ptáci se lekli rány a uletěli! 🦅",
    },
    {
        "otazka": "Kolik konců mají dvě a půl tyčky?",
        "moznosti": ["4", "5", "6", "3"],
        "spravna": 2,
        "vysvetleni": "Dvě tyčky mají 4 konce, půl tyčky má 2 → celkem 6! 🥢",
    },
    {
        "otazka": "Co je těžší? Tona peří, nebo tona cihel?",
        "moznosti": ["Cihly", "Peří", "Obojí váží stejně", "Záleží na větru"],
        "spravna": 2,
        "vysvetleni": "Obojí váží přesně jednu tunu. ⚖️",
    },

    # === NOVÉ ANO / NE OTÁZKY ===
    {
        "otazka": "Je možné, aby v Česku vycházelo slunce na západě?",
        "moznosti": ["Ano", "Ne"],
        "spravna": 1,
        "vysvetleni": "Slunce vychází na východě a zapadá na západě. 🌅",
    },
    {
        "otazka": "Můžeš přežít bez mozku déle než bez srdce?",
        "moznosti": ["Ano", "Ne"],
        "spravna": 1,
        "vysvetleni": "Bez mozku nelze přežít ani pár minut. Srdce může bít i bez mozku.",
    },
    {
        "otazka": "Je voda mokrá?",
        "moznosti": ["Ano", "Ne"],
        "spravna": 0,
        "vysvetleni": "Mokrost je vlastnost vody. Ano, voda je mokrá. 💧",
    },
    {
        "otazka": "Pokud vypneš všechna světla v místnosti, je tam tma?",
        "moznosti": ["Ano", "Ne"],
        "spravna": 0,
        "vysvetleni": "Ano, bez světla je tma. (Pokud nepočítáme okna atd.)",
    },
    {
        "otazka": "Má rok 366 dní?",
        "moznosti": ["Ano", "Ne"],
        "spravna": 1,
        "vysvetleni": "Pouze přestupný rok má 366 dní. Normální rok má 365.",
    },
    {
        "otazka": "Je možné, aby něco bylo zároveň větší a menší než něco jiného?",
        "moznosti": ["Ano", "Ne"],
        "spravna": 0,
        "vysvetleni": "Ano – např. 5 je větší než 3 a menší než 8.",
    },
    {
        "otazka": "Dokážeš stát zády k severu a zároveň čelem k severu?",
        "moznosti": ["Ano", "Ne"],
        "spravna": 0,
        "vysvetleni": "Ano – když stojíš na severním pólu.",
    },
]

class BrainTestApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🧠 Brain Test - Python Edice")
        self.geometry("720x650")
        self.resizable(False, False)

        self.otazky = []
        self.aktualni_index = 0
        self.skore = 0
        self.high_score = self.nacti_high_score()

        self.setup_ui()
        self.nova_hra()

    def setup_ui(self):
        # Horní panel
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=25, pady=(20, 5))

        self.label_titul = ctk.CTkLabel(
            top_frame, text="BRAIN TEST", font=ctk.CTkFont("Arial", 32, "bold"), text_color="#FFCC00"
        )
        self.label_titul.pack(side="left")

        self.label_progress = ctk.CTkLabel(top_frame, text="", font=ctk.CTkFont(size=16))
        self.label_progress.pack(side="right")

        self.label_skore = ctk.CTkLabel(self, text="Skóre: 0", font=ctk.CTkFont(size=18, weight="bold"))
        self.label_skore.pack(pady=(5, 15))

        # Karta otázky
        self.karta_otazky = ctk.CTkFrame(self, height=150, corner_radius=20)
        self.karta_otazky.pack(fill="x", padx=30, pady=15)
        self.karta_otazky.pack_propagate(False)

        self.label_otazka = ctk.CTkLabel(
            self.karta_otazky, text="", font=ctk.CTkFont(size=18, weight="bold"), wraplength=650
        )
        self.label_otazka.pack(expand=True, fill="both", padx=25, pady=25)

        # Tlačítka odpovědí
        self.tlacitka_odpovedi = []
        for i in range(4):
            btn = ctk.CTkButton(
                self,
                text="",
                font=ctk.CTkFont(size=16),
                height=58,
                corner_radius=12,
                command=lambda idx=i: self.zkontroluj_odpoved(idx),
            )
            btn.pack(pady=6, padx=50, fill="x")
            self.tlacitka_odpovedi.append(btn)

        # Výsledek
        self.label_vysledek = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=15), wraplength=650, justify="center"
        )
        self.label_vysledek.pack(pady=25, padx=30)

        # Tlačítko nová hra
        self.btn_nova_hra = ctk.CTkButton(
            self, text="🔄 Nová hra", font=ctk.CTkFont(size=16, weight="bold"),
            height=55, fg_color="#FFCC00", text_color="black", command=self.nova_hra
        )

    def nova_hra(self):
        self.otazky = random.sample(KNIHOVNA_OTAZEK, len(KNIHOVNA_OTAZEK))
        self.aktualni_index = 0
        self.skore = 0
        self.btn_nova_hra.pack_forget()
        self.nacti_otazku()

    def nacti_otazku(self):
        if self.aktualni_index >= len(self.otazky):
            self.ukonci_hru()
            return

        self.karta_otazky.configure(fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        self.label_vysledek.configure(text="")

        data = self.otazky[self.aktualni_index]
        pocet_moznosti = len(data["moznosti"])

        # Progress
        self.label_progress.configure(text=f"Otázka {self.aktualni_index + 1} / {len(self.otazky)}")

        self.label_otazka.configure(text=data["otazka"])

        # Zobrazíme jen potřebný počet tlačítek
        for i in range(4):
            if i < pocet_moznosti:
                self.tlacitka_odpovedi[i].configure(
                    text=data["moznosti"][i],
                    state="normal",
                    fg_color=("#3B82F6" if pocet_moznosti == 2 and i == 0 else  # Ano = modrá
                              "#EF4444" if pocet_moznosti == 2 and i == 1 else  # Ne = červená
                              ctk.ThemeManager.theme["CTkButton"]["fg_color"])
                )
                self.tlacitka_odpovedi[i].pack(pady=7, padx=50, fill="x")
            else:
                self.tlacitka_odpovedi[i].pack_forget()

    def zkontroluj_odpoved(self, volba: int):
        for btn in self.tlacitka_odpovedi:
            btn.configure(state="disabled")

        data = self.otazky[self.aktualni_index]

        if volba == data["spravna"]:
            self.skore += 1
            self.label_skore.configure(text=f"Skóre: {self.skore}")
            self.karta_otazky.configure(fg_color="#1E5F2B")
            self.label_vysledek.configure(text=f"✅ SPRÁVNĚ!\n{data['vysvetleni']}", text_color="#4ADE80")
        else:
            self.karta_otazky.configure(fg_color="#8B1E2F")
            self.label_vysledek.configure(text=f"❌ Chyták!\n{data['vysvetleni']}", text_color="#FF6B6B")

        self.aktualni_index += 1
        self.after(3200, self.nacti_otazku)

    def ukonci_hru(self):
        for btn in self.tlacitka_odpovedi:
            btn.pack_forget()

        if self.skore > self.high_score:
            self.high_score = self.skore
            self.uloz_high_score()

        # Hodnocení
        max_skore = len(KNIHOVNA_OTAZEK)
        if self.skore == max_skore:
            text = "🎉 ABSOLUTNÍ GÉNIUS! Jsi mozek roku!"
            color = "#FFCC00"
        elif self.skore >= max_skore * 0.75:
            text = "Výborný výkon! 🔥 Skvěle ti šly i Ano/Ne otázky."
            color = "#4ADE80"
        elif self.skore >= max_skore * 0.5:
            text = "Dobře zahráno!"
            color = "#FFCC00"
        else:
            text = "Zkus to znovu, chytáky jsou zrádné 😏"
            color = "#FF6B6B"

        self.label_titul.configure(text="KONEC HRY")
        self.label_skore.configure(
            text=f"{self.skore} z {max_skore} bodů\nNejlepší: {self.high_score}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label_vysledek.configure(text=text, text_color=color, font=ctk.CTkFont(size=17, weight="bold"))

        self.btn_nova_hra.pack(pady=30, padx=60, fill="x")

    # High score
    def nacti_high_score(self) -> int:
        try:
            return json.loads(Path("highscore.json").read_text(encoding="utf-8"))["highscore"]
        except:
            return 0

    def uloz_high_score(self):
        try:
            Path("highscore.json").write_text(
                json.dumps({"highscore": self.high_score}, ensure_ascii=False), encoding="utf-8"
            )
        except:
            pass


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = BrainTestApp()
    app.mainloop()