import os
file_text = "data_text.txt"

try:
    with open(file_text, "w", encoding="utf-8") as f:
        f.write("nějaký text.\n")
        f.write("toto je druhý řádek.\n")
    print(f"Soubor '{file_text}' byl úspěšně vytvořen a zapsán.")
except Exception as e:
    print(f"Došlo k chybě při práci se souborem: {e}")