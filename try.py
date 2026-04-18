# Simulace 2FA ochrany
def login_simulation():
    db_password = "MojeSilneHeslo123"
    db_otp_code = "5588" # Simulovaný kód z mobilu

    input_pass = input("Zadejte heslo: ")
    
    if input_pass == db_password:
        print("Heslo správné. Nyní zadejte kód z ověřovací aplikace.")
        input_code = input("Zadejte 4-místný kód: ")
        
        if input_code == db_otp_code:
            print("Přihlášení úspěšné!")
        else:
            print("Chyba: Útočník má heslo, ale nemá váš fyzický mobil!")
    else:
        print("Přístup zamítnut.")

login_simulation()