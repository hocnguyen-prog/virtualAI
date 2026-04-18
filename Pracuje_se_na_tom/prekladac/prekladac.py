import customtkinter as ctk
from deep_translator import GoogleTranslator
from datetime import datetime
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PrekladacApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CZ-VN Překladač s Historií")
        self.geometry("800x500") # Rozšířeno pro historii

        # Rozdělení na sloupce (Hlavní část a Historie)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- LEVÝ PANEL (Překladač) ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.label = ctk.CTkLabel(self.main_frame, text="Překladač", font=("Arial", 20, "bold"))
        self.label.pack(pady=10)

        self.direction_var = ctk.StringVar(value="cs -> vi")
        self.combo = ctk.CTkComboBox(self.main_frame, values=["cs -> vi", "vi -> cs"], variable=self.direction_var)
        self.combo.pack(pady=5)

        self.input_text = ctk.CTkTextbox(self.main_frame, height=100, width=300)
        self.input_text.pack(pady=10)

        self.btn = ctk.CTkButton(self.main_frame, text="Přeložit", command=self.prelozit)
        self.btn.pack(pady=5)

        self.output_text = ctk.CTkTextbox(self.main_frame, height=100, width=300)
        self.output_text.pack(pady=10)

        # --- PRAVÝ PANEL (Historie) ---
        self.history_frame = ctk.CTkFrame(self)
        self.history_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.hist_label = ctk.CTkLabel(self.history_frame, text="Historie překladů", font=("Arial", 16))
        self.hist_label.pack(pady=10)

        self.history_box = ctk.CTkTextbox(self.history_frame, width=350)
        self.history_box.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Načtení historie ze souboru při startu
        self.nacti_historii_ze_souboru()

    def uloz_do_historie(self, original, preklad, smer):
        cas = datetime.now().strftime("%d.%m. %H:%M")
        zaznam = f"[{cas}] ({smer}) {original} -> {preklad}\n"
        
        # Zápis do GUI
        self.history_box.insert("0.0", zaznam)
        
        # Zápis do souboru .txt
        with open("historie.txt", "a", encoding="utf-8") as f:
            f.write(zaznam)

    def nacti_historii_ze_souboru(self):
        if os.path.exists("historie.txt"):
            with open("historie.txt", "r", encoding="utf-8") as f:
                obsah = f.read()
                self.history_box.insert("1.0", obsah)

    def prelozit(self):
        smer = self.direction_var.get()
        src, tgt = smer.split(" -> ")
        vstup = self.input_text.get("1.0", "end-1c").strip()
        
        if not vstup:
            return

        try:
            preklad = GoogleTranslator(source=src, target=tgt).translate(vstup)
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", preklad)
            
            # Uložení
            self.uloz_do_historie(vstup, preklad, smer)
            
        except Exception as e:
            self.output_text.insert("1.0", f"Chyba: {e}")

if __name__ == "__main__":
    app = PrekladacApp()
    app.mainloop()