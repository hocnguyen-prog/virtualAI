import random
import time
import customtkinter as ctk

# Nastavení vzhledu aplikace
ctk.set_appearance_mode("dark")  # Režimy: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Témata: "blue", "green", "dark-blue"

# DATASETEK OTÁZEK (Knihovna)
# Každá otázka má text, seznam možností, index správné odpovědi (0-3) a vysvětlení (chyták)
KNIHOVNA_OTAZEK = [
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
        "spravna": 2,
        "vysvetleni": "Posledního nemůžeš předběhnout. Pokud ho předběhneš, nebyl poslední! 🏃",
    },
    {
        "otazka": "Co má dvě hlavy, čtyři oči, šest nohou a jeden ocas?",
        "moznosti": ["Kyklop na koni", "Jezdec na koni", "Dvouhlavý pes", "Ufon"],
        "spravna": 1,
        "vysvetleni": "Je to jezdec sedící na koni. Společně mají přesně tyto počty. 🐎",
    },
    {
        "otazka": "Kolik konců mají dvě a půl tyčky?",
        "moznosti": ["4", "5", "6", "3"],
        "spravna": 2,
        "vysvetleni": "Dvě tyčky mají 4 konce a ta poloviční má stále 2 konce. Celkem 6! 🥢",
    },
    {
        "otazka": "Otec Marušky má 5 dcer: Chacha, Cheche, Chichi, Chocho. Jak se jmenuje pátá?",
        "moznosti": ["Chuchu", "Maruška", "Chacha", "Neznámé"],
        "spravna": 1,
        "vysvetleni": "Je to přece otec Marušky! Stačí pozorně číst. 👧",
    },
    {
        "otazka": "Co je těžší? Tona peří, nebo tona cihel?",
        "moznosti": ["Cihly", "Peří", "Obojí váží stejně", "Záleží na větru"],
        "spravna": 2,
        "vysvetleni": "Obojí váží přesně jednu tonu. ⚖️",
    },
]


class BrainTestApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Brain Test - Python Edice")
        self.geometry("650x500")
        self.resizable(False, False)

        # Proměnné hry
        self.otazky = random.sample(KNIHOVNA_OTAZEK, len(KNIHOVNA_OTAZEK))
        self.aktualni_index = 0
        self.skore = 0

        # UI Prvky
        self.label_titul = ctk.CTkLabel(
            self, text="BRAIN TEST", font=("Arial", 28, "bold"), text_color="#FFCC00"
        )
        self.label_titul.pack(pady=15)

        self.label_skore = ctk.CTkLabel(
            self, text="Skóre: 0", font=("Arial", 14, "italic")
        )
        self.label_skore.pack(pady=5)

        # Hlavní karta pro otázku
        self.karta_otazky = ctk.CTkFrame(self, width=550, height=120, corner_radius=15)
        self.karta_otazky.pack_propagate(False)
        self.karta_otazky.pack(pady=15)

        self.label_otazka = ctk.CTkLabel(
            self.karta_otazky,
            text="",
            font=("Arial", 16, "bold"),
            wraplength=500,
        )
        self.label_otazka.pack(expand=True, fill="both", padx=10)

        # Tlačítka s odpověďmi
        self.tlacitka_odpovedi = []
        for i in range(4):
            btn = ctk.CTkButton(
                self,
                text="",
                font=("Arial", 14),
                width=400,
                height=45,
                corner_radius=10,
                command=lambda idx=i: self.zkontroluj_odpoved(idx),
            )
            btn.pack(pady=8)
            self.tlacitka_odpovedi.append(btn)

        # Label pro efekty a zpětnou vazbu
        self.label_vysledek = ctk.CTkLabel(
            self, text="", font=("Arial", 14, "bold"), wraplength=550
        )
        self.label_vysledek.pack(pady=20)

        # Spuštění první otázky
        self.nacti_otazku()

    def nacti_otazku(self):
        if self.aktualni_index < len(self.otazky):
            # Reset barvy karty otázky na původní temnou
            self.karta_otazky.configure(fg_color=["#E5E5E5", "#2B2B2B"])
            self.label_vysledek.configure(text="")

            # Aktivace tlačítek
            for btn in self.tlacitka_odpovedi:
                btn.configure(state="normal", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])

            data = self.otazky[self.aktualni_index]
            self.label_otazka.configure(text=data["otazka"])

            # Zamíchání nebo přiřazení možností
            for i, moznost in enumerate(data["moznosti"]):
                self.tlacitka_odpovedi[i].configure(text=moznost)
        else:
            self.ukonci_hru()

    def zkontroluj_odpoved(self, index_volby):
        # Deaktivace tlačítek, aby hráč neklikal během efektu
        for btn in self.tlacitka_odpovedi:
            btn.configure(state="disabled")

        data = self.otazky[self.aktualni_index]

        # EFEKT: Zelená/Červená reakce podle výsledku
        if index_volby == data["spravna"]:
            self.skore += 1
            self.label_skore.configure(text=f"Skóre: {self.skore}")
            self.karta_otazky.configure(fg_color="#2E7D32")  # Zelený záblesk
            self.label_vysledek.configure(
                text=f"SPRÁVNĚ! 🎉\n{data['vysvetleni']}", text_color="#4CAF50"
            )
        else:
            self.karta_otazky.configure(fg_color="#C62828")  # Červený záblesk
            self.label_vysledek.configure(
                text=f"CHYTÁK! ❌\n{data['vysvetleni']}", text_color="#F44336"
            )

        self.aktualni_index += 1
        # Efekt setrvání: Počkáme 3.5 sekundy, než načteme další otázku
        self.after(3500, self.nacti_otazku)

    def ukonci_hru(self):
        # Vyčištění obrazovky pro finální skóre
        self.karta_otazky.destroy()
        for btn in self.tlacitka_odpovedi:
            btn.destroy()

        self.label_otazka.destroy()

        # Zhodnocení
        if self.skore == len(KNIHOVNA_OTAZEK):
            hodnoceni = "Absolutní génius! 🧠✨"
            barva = "#FFCC00"
        elif self.skore >= len(KNIHOVNA_OTAZEK) // 2:
            hodnoceni = "Dobrá práce, ale chytáky tě občas dostaly! 😎"
            barva = "#4CAF50"
        else:
            hodnoceni = "Mno... logické myšlení dostalo zabrat. Zkus to znovu! 🙃"
            barva = "#F44336"

        self.label_titul.configure(text="KONEC HRY")
        self.label_skore.configure(
            text=f"Konečné skóre: {self.skore} z {len(KNIHOVNA_OTAZEK)}",
            font=("Arial", 20, "bold"),
        )

        self.label_vysledek.configure(
            text=hodnoceni, text_color=barva, font=("Arial", 16, "bold")
        )


if __name__ == "__main__":
    app = BrainTestApp()
    app.mainloop()