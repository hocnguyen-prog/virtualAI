Tady je **základní postup, jak se přihlásit ke GitHubu a nastavit repozitář v terminálu na Ubuntu/Linuxu** pomocí Git a GitHub.

---

# 1️⃣ Nainstaluj Git

Nejdřív zkontroluj, jestli máš Git:

```bash
git --version
```

Pokud není nainstalovaný:

```bash
sudo apt update
sudo apt install git
```

---

# 2️⃣ Nastav uživatelské údaje

Ty se ukládají globálně pro všechny repozitáře:

```bash
git config --global user.name "TvojeJmeno"
git config --global user.email "tvuj@email.cz"
```

Ověření:

```bash
git config --list
```

---

# 3️⃣ Přihlášení ke GitHubu (doporučeno přes SSH)

GitHub už nepodporuje klasické heslo → používá se **SSH klíč nebo token**.

### Vytvoř SSH klíč

```bash
ssh-keygen -t ed25519 -C "tvuj@email.cz"
```

Potvrď Enter u všech otázek.

---

### Spusť SSH agent

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

---

### Zkopíruj veřejný klíč

```bash
cat ~/.ssh/id_ed25519.pub
```

---

### Přidej ho do GitHubu

1. Otevři
   [https://github.com/settings/keys](https://github.com/settings/keys)

2. Klikni **New SSH Key**

3. vlož obsah klíče

---

### Otestuj připojení

```bash
ssh -T git@github.com
```

Pokud vše funguje, uvidíš zprávu typu:

```
Hi username! You've successfully authenticated.
```

---

# 4️⃣ Klonování repozitáře

```bash
git clone git@github.com:USERNAME/REPOSITORY.git
```

Například:

```bash
git clone git@github.com:jan123/muj-projekt.git
```

---

# 5️⃣ Vytvoření repozitáře z existující složky

```bash
cd muj-projekt
git init
git add .
git commit -m "first commit"
```

Přidání GitHub repozitáře:

```bash
git remote add origin git@github.com:USERNAME/REPOSITORY.git
```

Push:

```bash
git push -u origin main
```

---

# 6️⃣ Základní workflow

Ukládání změn:

```bash
git add .
git commit -m "popis změn"
git push
```

Stažení změn:

```bash
git pull
```

---

✅ Hotovo — repozitář je propojený s GitHubem.

---

💡 Pokud chceš, můžu ti taky ukázat:

* **nejjednodušší GitHub workflow (5 příkazů co používají programátoři denně)**
* **jak se přihlásit přes GitHub CLI (je to ještě jednodušší)**
* **jak nastavit Git tak, aby se už nikdy nemusel znovu přihlašovat**.
