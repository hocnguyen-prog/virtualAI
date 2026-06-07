# ai_agent_v2.py
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class AIAgent:
    def __init__(self, name="GrokAgent"):
        self.name = name
        self.memory = []
        self.tools = {
            "čas": self.get_time,
            "počítat": self.calculate,
            "wikipedia": self.search_wikipedia,
            "obecná_otázka": self.general_knowledge,
        }
    
    def get_time(self):
        return datetime.now().strftime("%d. %m. %Y, %H:%M:%S")
    
    def calculate(self, expr: str):
        try:
            return eval(expr, {"__builtins__": {}}, {"pow": pow})
        except:
            return "Chyba při výpočtu"
    
    def search_wikipedia(self, query: str):
        try:
            url = "https://cs.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_")
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                return data.get("extract", "Nenašel jsem informace.")
            return "Nenašel jsem stránku."
        except:
            return "Chyba při vyhledávání na Wikipedii."
    
    def general_knowledge(self):
        return "Momentálně nemám připojený velký jazykový model. Můžu ti ale pomoci přes nástroje (čas, počítání, Wikipedia)."
    
    def think(self, user_input: str) -> str:
        self.memory.append({"role": "user", "content": user_input})
        
        print(f"\n🤖 {self.name} přemýšlí...")
        
        # === ROZMYŠLENÍ (ReAct styl) ===
        lower = user_input.lower()
        
        thought = f"Otázka: {user_input}\n"
        
        if any(x in lower for x in ["čas", "hodina", "kolik je hodin"]):
            action = "čas"
            observation = self.get_time()
            response = f"Aktuální čas je **{observation}**."
            
        elif any(x in lower for x in ["spočítej", "vypočítej", "kolik je", "+", "plus", "minus"]):
            action = "počítat"
            expr = ''.join(c for c in user_input if c.isdigit() or c in '+-*/(). ')
            observation = self.calculate(expr)
            response = f"Výsledek: **{observation}**"
            
        elif any(x in lower for x in ["prezident", "prezidenta", "kancléř", "premier", "kdo je", "jméno", "jmenuje se", "hlava státu"]):
            action = "wikipedia"
            # Extrahujeme klíčová slova
            query = user_input.replace("jak se jmenuje", "").replace("kdo je", "").replace("prezident", "").replace("německa", "Německo").strip()
            observation = self.search_wikipedia(query or "Německo")
            response = observation
            
        else:
            action = "obecná_otázka"
            observation = "Žádný specializovaný tool"
            response = self.general_knowledge()
        
        print(f"   Myšlenka: Používám tool → {action}")
        print(f"   Výsledek toolu: {observation[:150]}..." if len(str(observation)) > 150 else f"   Výsledek toolu: {observation}")
        
        self.memory.append({"role": "assistant", "content": response})
        return response


# ==================== SPUŠTĚNÍ ====================
if __name__ == "__main__":
    agent = AIAgent("MůjChytrýAgent")
    
    print("🤖 Vylepšený AI Agent je připravený! (napiš 'konec' pro ukončení)\n")
    
    while True:
        user_input = input("👤 Ty: ")
        if user_input.lower() in ["konec", "exit", "quit", "bye"]:
            print("👋 Nashledanou!")
            break
        
        answer = agent.think(user_input)
        print(f"🤖 Agent: {answer}\n")