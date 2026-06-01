import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from crewai import Agent, Crew, Process, Task
from crewai.llms.providers.openai.completion import OpenAICompletion

DEFAULT_INVOICE_TEXT = """
Faktura číslo: 20260015
Dodavatel: TechCorp s.r.o., IČO: 12345678
Odběratel: Jan Novák, Praha
Datum splatnosti: 15. 6. 2026
Částka k úhradě: 15 400 Kč
Variabilní symbol: 20260015
Děkujeme za spolupráci.
"""


def serialize_result(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {k: serialize_result(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialize_result(v) for v in value]
    if hasattr(value, "dict"):
        try:
            return serialize_result(value.dict())
        except TypeError:
            pass
    if hasattr(value, "__dict__"):
        return serialize_result(vars(value))
    return str(value)


def build_agent(api_key: str | None = None) -> Agent:
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY není nastaven. Použijte --api-key nebo nastavte proměnnou prostředí."
        )

    llm = OpenAICompletion(model="gpt-4o", temperature=0.2, timeout=120)

    return Agent(
        role="Specialista na zpracování faktur",
        goal=(
            "Přesně analyzovat text faktury, vytáhnout klíčová data a připravit je pro účetní systém."
        ),
        backstory=(
            "Jsi precizní virtuální asistent, který nikdy nedělá chyby v číslech. "
            "Dokážeš v textu najít dodavatele, částku, variabilní symbol a měnu."
        ),
        verbose=True,
        llm=llm,
    )


def build_task(text: str, agent: Agent) -> Task:
    return Task(
        description=f"""
Zanalizuj následující text faktury a vytáhni z něj tyto informace:
- Název dodavatele
- Celková částka
- Měna
- Variabilní symbol

Text faktury ke zpracování:
{text}
""",
        expected_output=(
            "Strukturovaný JSON formát s klíči: dodavatel, castka, mena, variabilni_symbol."
        ),
        agent=agent,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Spustí fakturačního agenta a uloží výsledek do souboru."
    )
    parser.add_argument(
        "--input-file",
        "-i",
        type=Path,
        help="Cesta k souboru s textem faktury. Pokud není zadána, použije se výchozí text.",
    )
    parser.add_argument(
        "--text",
        "-t",
        help="Text faktury ke zpracování přímo z příkazové řádky.",
    )
    parser.add_argument(
        "--output-file",
        "-o",
        type=Path,
        default=Path("invoice_result.json"),
        help="Cesta, kam se uloží výsledný JSON.",
    )
    parser.add_argument(
        "--api-key",
        help="OpenAI API klíč. Pokud není zadán, použije se proměnná prostředí OPENAI_API_KEY.",
    )
    return parser.parse_args()


def load_invoice_text(args: argparse.Namespace) -> str:
    if args.text:
        return args.text
    if args.input_file:
        return args.input_file.read_text(encoding="utf-8")
    return DEFAULT_INVOICE_TEXT


def main() -> int:
    args = parse_args()
    invoice_text = load_invoice_text(args)

    agent = build_agent(api_key=args.api_key)
    task = build_task(invoice_text, agent)
    crew = Crew(agents=[agent], tasks=[task], process=Process.sequential)

    print("🤖 Agent začíná pracovat...")
    result = crew.kickoff()

    serialized = serialize_result(result)
    result_json = json.dumps(serialized, ensure_ascii=False, indent=2)

    output_path = args.output_file
    output_path.write_text(result_json, encoding="utf-8")

    print(f"✅ Výsledek byl uložen do: {output_path}")
    print("--- VÝSLEDNÝ REZULTÁT AGENTA ---")
    print(result_json)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
