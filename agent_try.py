import os
import sys
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
# Importujeme oficiální Google GenAI SDK
from google import genai
from google.genai import types

load_dotenv()

# Pokud běžíme ve Windows terminálu s omezeným kódováním, přepneme na UTF-8.
# Díky tomu se nevyhodí chyby při tisku emoji nebo češtiny.
try:
    if sys.stdout.encoding is None or sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
    if sys.stderr.encoding is None or sys.stderr.encoding.lower() != "utf-8":
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# Získání API klíče (musíš mít v .env souboru: GEMINI_API_KEY=tvoji_klic)
# Klíč získáš zdarma na: https://aistudio.google.com/
API_KEY = os.getenv("GEMINI_API_KEY")

class AIAgent:
    def __init__(self, name="GrokAgent", memory_file="agent_memory.json"):
        self.name = name
        self.memory_file = memory_file
        self.memory = self.load_memory()
        
        # Inicializace Gemini klienta
        self.client = None
        if not API_KEY:
            print("Varování: GEMINI_API_KEY nebyl nalezen v .env souboru. Agent nebude fungovat správně.")
        else:
            self.client = genai.Client(api_key=API_KEY)

        # Použijeme rychlý a schopný model Gemini 2.5 Flash
        self.model_name = "gemini-2.5-flash"

    def load_memory(self):
        """Načte dlouhodobou paměť ze souboru."""
        self.persistent_memory = []
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    self.persistent_memory = data.get("persistent_memory", []) or []
                    return data.get("conversation", []) or []
                return data
            except:
                return []
        return []

    def save_memory(self):
        """Uloží paměť do souboru (princip učení/pamatování)."""
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump({
                "conversation": self.memory,
                "persistent_memory": self.persistent_memory,
            }, f, ensure_ascii=False, indent=4)

    def remember_user_input(self, user_input: str):
        """Uloží důležité informace z uživatelova textu do trvalé paměti."""
        text = user_input.strip()
        if not text:
            return

        lower_text = text.lower()
        triggers = [
            "jsem", "mám", "můj", "moje", "mé", "mně", "mě",
            "rád", "ráda", "nejraději", "pracuji", "bydlím",
            "jmenuji se", "jmenuju se", "narodil", "narodila",
            "miluji", "potřebuji", "chci", "nechci"
        ]
        if any(trigger in lower_text for trigger in triggers):
            note = f"Uživatel řekl: {text}"
            if note not in self.persistent_memory:
                self.persistent_memory.append(note)

    def get_memory_summary(self) -> str:
        """Vrátí stručný souhrn trvalé paměti pro systémovou instrukci."""
        if not self.persistent_memory:
            return ""
        summary_lines = [f"- {item}" for item in self.persistent_memory[-20:]]
        return "Trvalá paměť:\n" + "\n".join(summary_lines) + "\n\n"

    # === NÁSTROJE (TOOLS), KTERÉ MÁ AGENT K DISPOZICI ===
    
    def get_time(self) -> str:
        """Vrátí aktuální datum a čas."""
        return datetime.now().strftime("%d. %m. %Y, %H:%M:%S")
    
    def calculate(self, expression: str) -> str:
        """Vypočítá matematický výraz. Příklad: '2 + 2 * 5'"""
        try:
            # Bezpečné vyhodnocení matematického výrazu
            result = eval(expression, {"__builtins__": {}}, {"pow": pow})
            return f"Výsledek je {result}"
        except:
            return "Chyba: Neplatný matematický výraz."
    
    def search_wikipedia(self, query: str) -> str:
        """Vyhledá informace na české Wikipedii pro zadané téma."""
        try:
            url = "https://cs.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_")
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                return data.get("extract", "Nenašel jsem podrobnosti.")
            return f"O tématu '{query}' jsem na Wikipedii nic nenašel."
        except:
            return "Došlo k chybě při komunikaci s Wikipedií."

    def think(self, user_input: str) -> str:
        print(f"\n🤖 {self.name} přemýšlí a rozhoduje se...")
        
        if self.client is None:
            return "Chybí GEMINI_API_KEY. Nastav prosím klíč v souboru .env jako GEMINI_API_KEY."

        # Zapamatuj si, co uživatel říká do trvalé paměti
        self.remember_user_input(user_input)

        # Přidáme aktuální zprávu od uživatele do paměti konverzace
        self.memory.append({"role": "user", "parts": [{"text": user_input}]})
        
        # Definujeme nástroje pro Gemini (předáme samotné Python funkce)
        available_tools = [self.get_time, self.calculate, self.search_wikipedia]
        
        # Systémová instrukce, která agentovi říká, jak se má chovat
        memory_summary = self.get_memory_summary()
        system_instruction = (
            f"{memory_summary}Jsi autonomní AI agent jménem {self.name}. Máš přístup k nástrojům. "
            "Pokud k odpovědi potřebuješ čas, výpočet nebo Wikipedii, použij příslušný nástroj. "
            "Pamatuj si, co ti uživatel říká, tvá paměť je trvalá. Odpovídej vždy v češtině."
        )

        try:
            # Voláme LLM a předáváme mu celou historii i nástroje
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=self.memory,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=available_tools, # LLM vidí tyto funkce a jejich popisy
                    temperature=0.3
                )
            )
            
            # Kontrola, zda model chce spustit nějaký nástroj (Function Calling)
            if response.function_calls:
                for call in response.function_calls:
                    tool_name = call.name
                    args = call.args
                    
                    print(f"   ↳ 🛠️ Model se rozhodl použít nástroj: {tool_name} s argumenty: {dict(args)}")
                    
                    # Spuštění správného nástroje podle volání modelu
                    if tool_name == "get_time":
                        observation = self.get_time()
                    elif tool_name == "calculate":
                        observation = self.calculate(args.get("expression"))
                    elif tool_name == "search_wikipedia":
                        observation = self.search_wikipedia(args.get("query"))
                    else:
                        observation = "Neznámý nástroj."

                    print(f"   ↳ 👁️ Výsledek nástroje: {observation[:100]}...")

                    # Poskytneme výsledky nástroje zpět modelu, aby vygeneroval finální odpověď pro uživatele
                    # Nejprve mu musíme poslat to, že o ten nástroj požádal:
                    self.memory.append({"role": "model", "parts": [types.Part.from_function_call(name=call.name, args=call.args)]})
                    # A následně výsledek (Observation)
                    self.memory.append({
                        "role": "tool",
                        "parts": [types.Part.from_function_response(name=call.name, response={"result": observation})]
                    })
                    
                    # Druhé volání modelu, aby zpracoval výsledek nástroje do lidské řeči
                    final_response = self.client.models.generate_content(
                        model=self.model_name,
                        contents=self.memory,
                        config=types.GenerateContentConfig(system_instruction=system_instruction)
                    )
                    
                    agent_reply = final_response.text
            else:
                # Model nepotřeboval žádný nástroj a odpověděl rovnou ze svých znalostí
                agent_reply = response.text

            # Uložíme odpověď agenta do paměti a zapíšeme na disk
            self.memory.append({"role": "model", "parts": [{"text": agent_reply}]})
            self.save_memory()
            
            return agent_reply

        except Exception as e:
            return f"Omlouvám se, došlo k chybě při komunikaci s mozkem agenta: {e}"


# ==================== SPUŠTĚNÍ ANGAŽMÁ ====================
if __name__ == "__main__":
    # Vytvoření agenta
    agent = AIAgent("ChytrýAgentV3")
    
    print(f"🤖 Agent {agent.name} je online a učí se!")
    print(f"Počet načtených zpráv z historie: {len(agent.memory)}")
    print("(Napiš 'konec' pro ukončení)\n")
    
    while True:
        user_input = input("👤 Ty: ")
        if user_input.lower() in ["konec", "exit", "quit", "bye"]:
            print("👋 Nashledanou! Moje paměť je uložena.")
            break
        
        if not user_input.strip():
            continue
            
        answer = agent.think(user_input)
        print(f"🤖 Agent: {answer}\n")