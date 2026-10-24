import sys
import time
from currans_idea.engine import CurransIdeaEngine
from currans_idea.channel_parser import ChannelPostParser

# vedere protocolli telegram dopo
def read_input():
    print("[Incolla il post o evento (premi INVIO due volte per inviare, o 'exit')]")
    lines = []
    while True:
        try:
            line = input()
            if not line:
                if lines:
                    break
                else:
                    continue
            if line.strip().lower() in ["exit", "quit", "q"] and not lines:
                return "exit"
            lines.append(line)
        except (KeyboardInterrupt, EOFError):
            return "exit"
    return "\n".join(lines).strip()

def main():
    engine = CurransIdeaEngine()

    print("=" * 65)
    print("  Curran's Idea - Intelligent Channel Post Comment Simulator")
    print("  Parser Canale + 5 Archetipi Comportamentali")
    print("=" * 65)

    while True:
        event = read_input()
        if event == "exit":
            print("\nesco")
            break
        if not event:
            continue

        print(f"\n--- RISPOSTE SIMULATE PER IL POST ---")
        reactions = engine.simulate_mock_reactions(event)

        for r in reactions:
            print(f"[+{r['delay_seconds']}s] ({r['persona_name']})")
            print(f"       > {r['message']}\n")

if __name__ == "__main__":
    main()
