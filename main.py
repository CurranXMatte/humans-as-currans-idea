import sys
import argparse
from currans_idea.engine import CurransIdeaEngine
from currans_idea.channel_parser import ChannelPostParser

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

def run_interactive(engine):
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

def main():
    parser = argparse.ArgumentParser(description="Curran's Idea - Telegram Channel & Group Behavioral Engine")
    parser.add_argument("--serve", action="store_true", help="Avvia il server REST API FastAPI su porta 8000")
    parser.add_argument("--host", default="0.0.0.0", help="Host per il server API (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Porta per il server API (default: 8000)")
    parser.add_argument("--post", type=str, help="Simula reazioni per un post singolo specificato da riga di comando")
    parser.add_argument("--thread", type=str, help="Simula una discussione a catena multi-turno bot-to-bot sotto il post")

    args = parser.parse_args()
    engine = CurransIdeaEngine()

    if args.serve:
        import uvicorn
        print(f"🚀 Avvio FastAPI server su http://{args.host}:{args.port}")
        print(f"📖 Swagger UI interattiva disponibile su: http://localhost:{args.port}/docs")
        uvicorn.run("currans_idea.api:app", host=args.host, port=args.port, reload=False)
        return

    if args.post:
        reactions = engine.simulate_mock_reactions(args.post)
        print(f"\n--- REAZIONI AL POST ---")
        for r in reactions:
            print(f"[+{r['delay_seconds']}s] ({r['persona_name']})")
            print(f"       > {r['message']}\n")
        return

    if args.thread:
        thread = engine.simulate_thread(args.thread)
        print(f"\n--- THREAD MULTI-TURNO ---")
        for t in thread:
            reply_info = f" (in risposta a #{t['in_reply_to_id']} {t['in_reply_to_persona']})" if t['in_reply_to_id'] else " (Post Canale)"
            print(f"[#{t['id']} | +{t['delay_seconds']}s]{reply_info} {t['persona_name']}:")
            print(f"       > {t['message']}\n")
        return

    run_interactive(engine)

if __name__ == "__main__":
    main()
