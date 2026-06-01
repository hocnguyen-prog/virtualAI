from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

app = FastAPI(title="UniEdu Core API 2026")

# --- MODELY (Založeno na ERD schématu [7]) ---

class Kriterium(BaseModel):
    id: str
    tema: str # "Na čem žák pracoval" [8]
    dosazeno: str # "Jak se mu dařilo" [9]

class Student(BaseModel):
    id: str
    jmeno: str
    prijmeni: str
    email: EmailStr
    trida_id: str
    slovni_hodnoceni: Optional[str] = None
    kriteria: List[Kriterium] = Field(default_factory=list)

# --- AMBIENTNÍ AI LOGIKA (Trend 2026 [3]) ---

def generuj_slovni_analyzu(student: Student):
    """
    Simulace Ambientní AI, která z 'naklikaných' kritérií 
    sestaví příběh (Narrative Interface [10]).
    """
    if not student.kriteria:
        return "Zatím nebyla zadána žádná kritéria."
    
    uvod = f"Student {student.jmeno} se v tomto pololetí zaměřil na: "
    temata = ", ".join([k.tema for k in student.kriteria])
    return uvod + temata + ". Celkově dosáhl výborných výsledků."

# --- API ENDPOINTY ---

@app.get("/studenti/{student_id}", response_model=Student)
async def ziskej_kartu_zaka(student_id: str):
    # Simulace databáze (v reálu PostgreSQL + Prisma [11])
    return Student(
        id=student_id, 
        jmeno="Jan", 
        prijmeni="Novák", 
        email="jan.novak@skola.cz",
        trida_id="4.A",
        kriteria=[Kriterium(id="1", tema="Poznáváme plazy", dosazeno="Rozpozná nejběžnější plazy [12]")]
    )

@app.post("/hodnoceni/automatizace")
async def vytvor_slovni_hodnoceni(student: Student):
    """Vytvoří návrh hodnocení bez nutnosti psaní dlouhých odstavců [13]."""
    navrh = generuj_slovni_analyzu(student)
    return {"navrh_textu": navrh}
