# prekladac
import re
import os
import sys


def nacist_soubor(nazev_souboru):
    """Načte obsah souboru."""
    try:
        with open(nazev_souboru, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Chyba: Soubor '{nazev_souboru}' nebyl nalezen.")
        return None
    except Exception as e:
        print(f"Chyba při čtení souboru: {e}")
        return None


def zapsat_soubor(nazev_souboru, obsah):
    """Zapíše obsah do souboru."""
    try:
        with open(nazev_souboru, 'w', encoding='utf-8') as f:
            f.write(obsah)
        print(f"Soubor '{nazev_souboru}' byl úspěšně uložen.")
        return True
    except Exception as e:
        print(f"Chyba při zápisu do souboru: {e}")
        return False


def prelozit_klicova_slova(kod):
    """Překládá klíčová slova z čeština do ASCII."""
    preklad_dict = {
        r'\bkalkulačka\b': 'kalkulacka',
        r'\bSčítání\b': 'Scitani',
        r'\bOdčítání\b': 'Odcitani',
        r'\bNásobení\b': 'Nasobeni',
        r'\bDělení\b': 'Deleni',
        r'\bVýsledek\b': 'Vysledek',
        r'\bChyba\b': 'Chyba',
        r'\bFunkce\b': 'Funkce',
    }
    
    vysledek = kod
    for ceske, ascii_verze in preklad_dict.items():
        vysledek = re.sub(ceske, ascii_verze, vysledek)
    
    return vysledek


def prelozit_znaky(kod):
    """Překládá speciální znaky na ASCII ekvivalenty."""
    znaky_dict = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'ů': 'u', 'ý': 'y', 'ř': 'r', 'š': 's', 'ž': 'z',
        'č': 'c', 'ť': 't', 'ň': 'n', 'ď': 'd',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'Ů': 'U', 'Ý': 'Y', 'Ř': 'R', 'Š': 'S', 'Ž': 'Z',
        'Č': 'C', 'Ť': 'T', 'Ň': 'N', 'Ď': 'D',
    }
    
    vysledek = kod
    for cesky, ascii_char in znaky_dict.items():
        vysledek = vysledek.replace(cesky, ascii_char)
    
    return vysledek


def prekladac(input_file, output_file):
    """Hlavní funkce pro překlad souboru."""
    kod = nacist_soubor(input_file)
    
    if kod is None:
        return False
    
    # Aplikuj překlady
    kod = prelozit_klicova_slova(kod)
    kod = prelozit_znaky(kod)
    
    # Ulož výsledek
    return zapsat_soubor(output_file, kod)


def statistika_prekladu(puvodni, prelozeny):
    """Vypočítá statistiku překladu."""
    puvodni_delka = len(puvodni)
    prelozeny_delka = len(prelozeny)
    rozdil = puvodni_delka - prelozeny_delka
    
    print(f"--- Statistika překladu ---")
    print(f"Původní délka: {puvodni_delka} znaků")
    print(f"Přeložená délka: {prelozeny_delka} znaků")
    print(f"Rozdíl: {rozdil} znaků")
    print(f"Změna: {(rozdil/puvodni_delka*100):.2f}%" if puvodni_delka > 0 else "N/A")


def validovat_soubor(nazev_souboru):
    """Ověří, zda soubor existuje a je čitelný."""
    if not os.path.exists(nazev_souboru):
        print(f"Chyba: Soubor '{nazev_souboru}' neexistuje.")
        return False
    
    if not os.path.isfile(nazev_souboru):
        print(f"Chyba: '{nazev_souboru}' není soubor.")
        return False
    
    return True


def main():
    """Hlavní funkce programu."""
    if len(sys.argv) < 3:
        print("Uso: python prekladac.py <vstupní_soubor> <výstupní_soubor>")
        sys.exit(1)
    
    vstup = sys.argv[1]
    vystup = sys.argv[2]
    
    if not validovat_soubor(vstup):
        sys.exit(1)
    
    print(f"Překládám soubor '{vstup}' do '{vystup}'...")
    if prekladac(vstup, vystup):
        print("Překlad dokončen!")
    else:
        print("Překlad selhal.")
        sys.exit(1)


if __name__ == "__main__":
    main()
    