import random
import json
from pathlib import Path
import customtkinter as ctk
from typing import List, Dict


# ====================== DATA ======================
# Seznam všech otázek (knihovna)
KNIHOVNA_OTAZEK: List[Dict] = [
    {
        "otazka": "Na stromě sedí 5 ptáků. Lovec jednoho zastřelí. Kolik ptáků zůstalo?",
        "moznosti": ["4", "5", "0", "1"],
        "spravna": 2,
        "vysvetleni": "Ostatní ptáci se lekli rány a uletěli! 🦅",
    },
    {
        "otazka": "Některé měsíce mají 31 dní, některé 30. Kolik měsíců má 28 dní?",
        "moznosti": ["1", "2", "6", "Všechny"],
        "spravna": 3,
        "vysvetleni": "Každý měsíc v roce má přece alespoň 28 dní! 📅",
    },
    {
        "otazka": "Předběhneš posledního závodníka v běhu. Na jaké pozici teď jsi?",
        "moznosti": ["Předposlední", "Poslední", "Nelze ho předběhnout", "První"],
        "spravna": 1,
        "vysvetleni": "Jakmile ho předběhneš, už není poslední. Jsi tedy poslední ty! 🏃",
    },
    {
        "otazka": "Co má dvě hlavy, čtyři oči, šest nohou a jeden ocas?",
        "moznosti": ["Kyklop na koni", "Jezdec na koni", "Dvouhlavý pes", "Ufon"],
        "spravna": 1,
        "vysvetleni": "Jezdec sedící na koni. Společně mají tyto počty. 🐎",
    },
    {
        "otazka": "Kolik konců mají dvě a půl tyčky?",
        "moznosti": ["4", "5", "6", "3"],
        "spravna": 2,
        "vysvetleni": "Dvě celé tyčky = 4 konce, půl tyčky = 2 konce → celkem 6! 🥢",
    },
    {
        "otazka": "Otec Marušky má 5 dcer: Chacha, Cheche, Chichi, Chocho. Jak se jmenuje pátá?",
        "moznosti": ["Chuchu", "Maruška", "Chacha", "Neznámé"],
        "spravna": 1,
        "vysvetleni": "Pátá dcera se jmenuje Maruška! 👧",
    },
    {
        "otazka": "Co je těžší? Tona peří, nebo tona cihel?",
        "moznosti": ["Cihly", "Peří", "Obojí váží stejně", "Záleží na větru"],
        "spravna": 2,
        "vysvetleni": "Obojí váží přesně jednu tunu. ⚖️",
    },
]


class BrainTestApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🧠 Brain Test - Python Edice")
        self.geometry("700x620")
        self.resizable(False, False)

        # Proměnné hry
        self.otazky = []                # Aktuální zamíchaný seznam otázek
        self.aktualni_index = 0         # Číslo aktuální otázky
        self.skore = 0                  # Počet správných odpovědí
        self.high_score = self.nacti_high_score()  # Nejlepší skóre z minulých her

        self.setup_ui()                 # Vytvoření grafického rozhraní
        self.nova_hra()                 # Spuštění nové hry


    def setup_ui(self):
        """Vytvoření a nastavení všech prvků uživatelského rozhraní"""
        
        # === Horní panel ===
        top_frame = ctk.CTkFrame(self, height=80, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=(15, 5))

        self.label_titul = ctk.CTkLabel(
            top_frame, text="BRAIN TEST", font=ctk.CTkFont("Arial", 32, "bold"), text_color="#FFCC00"
        )
        self.label_titul.pack(side="left")

        self.label_progress = ctk.CTkLabel(
            top_frame, text="", font=ctk.CTkFont("Arial", 16)
        )
        self.label_progress.pack(side="right")

        # Skóre
        self.label_skore = ctk.CTkLabel(
            self, text="Skóre: 0", font=ctk.CTkFont("Arial", 18, "bold")
        )
        self.label_skore.pack(pady=(5, 10))

        # Karta s otázkou
        self.karta_otazky = ctk.CTkFrame(self, height=140, corner_radius=20)
        self.karta_otazky.pack(fill="x", padx=30, pady=15)
        self.karta_otazky.pack_propagate(False)

        self.label_otazka = ctk.CTkLabel(
            self.karta_otazky,
            text="",
            font=ctk.CTkFont("Arial", 18, "bold"),
            wraplength=620,
        )
        self.label_otazka.pack(expand=True, fill="both", padx=25, pady=20)

        # Tlačítka s odpověďmi (4 ks)
        self.tlacitka_odpovedi = []
        for i in range(4):
            btn = ctk.CTkButton(
                self,
                text="",
                font=ctk.CTkFont("Arial", 15),
                height=55,
                corner_radius=12,
                command=lambda idx=i: self.zkontroluj_odpoved(idx),
            )
            btn.pack(pady=6, padx=40, fill="x")
            self.tlacitka_odpovedi.append(btn)

        # Label pro výsledek a vysvětlení
        self.label_vysledek = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont("Arial", 15),
            wraplength=620,
            justify="center",
        )
        self.label_vysledek.pack(pady=20, padx=30)

        # Tlačítko pro novou hru (zobrazuje se až na konci)
        self.btn_nova_hra = ctk.CTkButton(
            self,
            text="🔄 Nová hra",
            font=ctk.CTkFont("Arial", 16, "bold"),
            height=50,
            fg_color="#FFCC00",
            text_color="black",
            command=self.nova_hra,
        )


    def nova_hra(self):
        """Začne úplně novou hru"""
        self.otazky = random.sample(KNIHOVNA_OTAZEK, len(KNIHOVNA_OTAZEK))  # Zamíchání otázek
        self.aktualni_index = 0
        self.skore = 0

        self.btn_nova_hra.pack_forget()                    # Skryje tlačítko nové hry

        # Reset vzhledu
        self.karta_otazky.configure(fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        self.label_vysledek.configure(text="")
        self.label_skore.configure(text="Skóre: 0")

        for btn in self.tlacitka_odpovedi:
            btn.configure(state="normal")

        self.nacti_otazku()


    def nacti_otazku(self):
        """Načte a zobrazí další otázku"""
        if self.aktualni_index >= len(self.otazky):
            self.ukonci_hru()
            return

        # Reset barev a stavu
        self.karta_otazky.configure(fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        self.label_vysledek.configure(text="")

        # Aktivace všech tlačítek
        for btn in self.tlacitka_odpovedi:
            btn.configure(state="normal", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])

        data = self.otazky[self.aktualni_index]

        # Zobrazení progresu
        self.label_progress.configure(
            text=f"Otázka {self.aktualni_index + 1} / {len(self.otazky)}"
        )

        self.label_otazka.configure(text=data["otazka"])

        # Naplnění tlačítek možnostmi
        for i, moznost in enumerate(data["moznosti"]):
            self.tlacitka_odpovedi[i].configure(text=moznost)


    def zkontroluj_odpoved(self, volba: int):
        """Zpracuje vybranou odpověď hráče"""
        # Deaktivace tlačítek aby hráč nemohl klikat víckrát
        for btn in self.tlacitka_odpovedi:
            btn.configure(state="disabled")

        data = self.otazky[self.aktualni_index]
        spravne = data["spravna"]

        if volba == spravne:
            self.skore += 1
            self.label_skore.configure(text=f"Skóre: {self.skore}")
            self.karta_otazky.configure(fg_color="#1E5F2B")           # Zelená
            self.label_vysledek.configure(
                text=f"✅ SPRÁVNĚ!\n{data['vysvetleni']}",
                text_color="#4ADE80"
            )
        else:
            self.karta_otazky.configure(fg_color="#8B1E2F")            # Červená
            self.label_vysledek.configure(
                text=f"❌ Chyták!\n{data['vysvetleni']}",
                text_color="#FF6B6B"
            )

        self.aktualni_index += 1
        # Po 3,2 sekundách načte další otázku
        self.after(3200, self.nacti_otazku)


    def ukonci_hru(self):
        """Zobrazí výsledky po dokončení všech otázek"""
        for widget in self.tlacitka_odpovedi:
            widget.configure(state="disabled")

        # Uložení high score
        if self.skore > self.high_score:
            self.high_score = self.skore
            self.uloz_high_score()

        # Hodnocení podle skóre
        max_skore = len(KNIHOVNA_OTAZEK)
        if self.skore == max_skore:
            text = "🎉 ABSOLUTNÍ GÉNIUS! 🎉\nJsi mozek roku!"
            color = "#FFCC00"
        elif self.skore >= max_skore * 0.7:
            text = "Velmi dobrý výkon! 🔥\nSkoro jsi to dal!"
            color = "#4ADE80"
        elif self.skore >= max_skore * 0.5:
            text = "Solidní výsledek, ale ještě je prostor na zlepšení."
            color = "#FFCC00"
        else:
            text = "Příště to dáš líp!\nChytáky jsou zrádné 😏"
            color = "#FF6B6B"

        self.label_titul.configure(text="KONEC HRY")
        self.label_skore.configure(
            text=f"{self.skore} z {max_skore} bodů\nNejlepší skóre: {self.high_score}",
            font=ctk.CTkFont("Arial", 20, "bold")
        )
        self.label_vysledek.configure(text=text, text_color=color, font=ctk.CTkFont("Arial", 18, "bold"))

        self.btn_nova_hra.pack(pady=30, padx=40, fill="x")


    # ==================== HIGH SCORE ====================
    def nacti_high_score(self) -> int:
        """Načte nejlepší skóre ze souboru"""
        try:
            path = Path("highscore.json")
            if path.exists():
                return json.loads(path.read_text(encoding="utf-8"))["highscore"]
        except:
            pass
        return 0


    def uloz_high_score(self):
        """Uloží nejlepší skóre do souboru"""
        try:
            data = {"highscore": self.high_score}
            Path("highscore.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        except:
            pass


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    app = BrainTestApp()
    app.mainloop()