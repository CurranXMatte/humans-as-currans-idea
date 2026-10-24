#!/usr/bin/env python3
"""
Humans as Curran's Idea - Interactive CLI Playground
"""
import sys
import time
from currans_idea.engine import CurransIdeaEngine

def main():
    engine = CurransIdeaEngine()

    print("=" * 65)
    print("  HUMANS AS CURRAN'S IDEA — Telegram Bot Persona Simulator")
    print("  Calibrated on 3,856 real chat messages | v2.0")
    print("=" * 65)
    print("Digita un evento calcistico (es: 'Gol inter 1-0 calhanoglu', 'Rigore sbagliato', 'Espulsione theo')")
    print("oppure 'exit' per uscire.\n")

    while True:
        try:
            event = input("\n[Evento / Post Canale] > ").strip()
            if not event:
                continue
            if event.lower() in ["exit", "quit", "q"]:
                print("Chiusura simulatore. Ciao!")
                break

            print(f"\n--- Simulazione risposte per: '{event}' ---")
            reactions = engine.simulate_mock_reactions(event)

            for r in reactions:
                print(f"[+{r['delay_seconds']}s] ({r['persona_name']})")
                print(f"       > {r['message']}\n")

        except KeyboardInterrupt:
            print("\nUscita.")
            break
        except Exception as e:
            print(f"Errore: {e}")

if __name__ == "__main__":
    main()
