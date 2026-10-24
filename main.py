import sys
import time
from currans_idea.engine import CurransIdeaEngine

# vedere protocolli telegram dopo
def main():
    engine = CurransIdeaEngine()

    print("=" * 60)
    print("  Curran's Idea - Test Bot Personas")
    print("=" * 60)
    print("Scrivi un evento (es: 'Gol inter', 'Rigore sbagliato') o 'exit'\n")

    while True:
        try:
            event = input("[evento] > ").strip()
            if not event:
                continue
            if event.lower() in ["exit", "quit", "q"]:
                break

            print(f"\n--- risposte per: '{event}' ---")
            reactions = engine.simulate_mock_reactions(event)

            for r in reactions:
                print(f"[+{r['delay_seconds']}s] ({r['persona_name']})")
                print(f"       > {r['message']}\n")

        except KeyboardInterrupt:
            print("\nesco")
            break
        except Exception as e:
            print(f"err: {e}")

if __name__ == "__main__":
    main()
