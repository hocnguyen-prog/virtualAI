# kalkulačka

def kalkulacka():
    print(f"kalkulačka\n1. Sčítání\n2. Odčítání\n3. Násobení\n4. Dělení")
    volba = input("Vyberte operaci (1/2/3/4): ")

    try:
        num1 = float(input("Zadejte první číslo: "))
        num2 = float(input("Zadejte druhé číslo: "))
    except ValueError:
        print("Neplatné číslo.")
        return

    if volba == '1':
        print(f"{num1} + {num2} = {num1 + num2}")
    elif volba == '2':
        print(f"{num1} - {num2} = {num1 - num2}")
    elif volba == '3':
        print(f"{num1} * {num2} = {num1 * num2}")
    elif volba == '4':
        if num2 != 0:
            print(f"{num1} / {num2} = {num1 / num2}")
        else:
            print("Dělení nulou není povoleno.")
    else:
        print("Neplatná volba.")


if __name__ == "__main__":
    kalkulacka() 