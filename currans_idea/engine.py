"""
Core engine orchestrating persona reactions, latency delays, and heuristic filtering.
"""
import random
from typing import Dict, List, Any
from .personas import PERSONAS
from .validators import validate_and_clean

class CurransIdeaEngine:
    def __init__(self, personas_config: Dict[int, Any] = None):
        self.personas = personas_config or PERSONAS

    def get_delays(self) -> Dict[int, int]:
        """Calculates randomized human-like reaction delays for each persona."""
        delays = {}
        for pid, pdata in self.personas.items():
            low, high = pdata["delay_range"]
            delays[pid] = random.randint(low, high)
        return delays

    def format_prompt_for_llm(self, event_text: str, persona_id: int) -> str:
        """Generates a specialized system/user prompt for an LLM to produce a calibrated response."""
        p = self.personas[persona_id]
        examples = "\n".join(f"- {s}" for s in p["sample_responses"])
        
        prompt = f"""Tu sei un utente reale in una chat Telegram di calcio tra ragazzi.
Devi reagire a questo evento: "{event_text}"

Identità comportamentale: {p['name']}
Descrizione: {p['description']}
Regole di stile: {p['style_guide']}
Vincolo parole: da {p['min_words']} a massimo {p['max_words']} parole.
DIVIETO ASSOLUTO:
- NON mettere mai il punto fermo finale
- NON usare gergo da giornalista TV ("i cugini", "compagine", "derby della madonnina", "telefonatissimo")
- NON inserire emoji forzate a fine frase

Esempi di risposte realistiche per il tuo profilo:
{examples}

Genera solo la tua risposta, nient'altro:"""
        return prompt

    def simulate_mock_reactions(self, event_text: str) -> List[Dict[str, Any]]:
        """
        Returns ready-to-display simulated responses for the given event,
        using calibrated archetypes and realistic delays.
        """
        event_lower = event_text.lower()
        delays = self.get_delays()
        results = []

        is_goal = "gol" in event_lower or "rete" in event_lower
        is_miss = "sbagliato" in event_lower or "errore" in event_lower or "palo" in event_lower or "fuori" in event_lower
        is_card = "rosso" in event_lower or "espulso" in event_lower or "giallo" in event_lower

        for pid in sorted(self.personas.keys()):
            p = self.personas[pid]
            delay = delays[pid]

            # Generate contextual realistic response
            if pid == 1: # Emotivo
                if is_goal:
                    msg = random.choice(["SEEEEEEE PROPRIO LUI GODOOO", "MAMMA MIA CHE GIOCATORE SEEE", "GODOOOO FINALMENTE"])
                elif is_miss:
                    msg = random.choice(["NON CI CREDO MA COME SI FA DAI", "MA VAI A CAGARE VA", "IN POZZO SENZA FONDO NON CI CREDO"])
                else:
                    msg = random.choice(["NON CI CREDO", "MAMMA MIA", "MA CHE ROBA È"])

            elif pid == 2: # Cinico
                if is_goal:
                    msg = random.choice(["difesa imbarazzante comunque dormivano tutti", "gol a culo tanto mo pareggiano", "non esaltatevi che fan cagare entrambi"])
                elif is_miss:
                    msg = random.choice(["rigore osceno comunque giocatore pippissimo", "paracarro inutile come sempre", "non segna manco a porta vuota questo"])
                else:
                    msg = random.choice(["partita oscena comunque", "arbitro comprato sicuro"])

            elif pid == 3: # Troll
                if is_goal:
                    msg = random.choice(["questo gli esulta pure in faccia godo ahahahah", "tutti zitti adesso dai", "manco con le mani la prendeva ahahah"])
                elif is_miss:
                    msg = random.choice(["ma dove cazzo voleva tirarlo ahahahah", "pallone sulla luna ahahah", "nemmeno su fifa uno scempio simile"])
                else:
                    msg = random.choice(["ma chi cazzo è questo ahahah", "pagliacci totali"])

            elif pid == 4: # Fanta
                if is_goal:
                    msg = random.choice(["ovvio che mi segna contro al fanta sto maledetto", "assist confermato o l'hanno tolto?", "ce l'ho contro porco dio"])
                elif is_miss:
                    msg = random.choice(["ovvio mi ha bruciato la schedina sto cane", "messo titolare al fanta per sto -3", "ho perso la bolla per colpa sua"])
                else:
                    msg = random.choice(["fantacalcio distrutto per colpa sua", "quanto prende secondo voi?"])

            elif pid == 5: # Telegrafico
                if is_goal:
                    msg = random.choice(["godo", "meritato", "finita"])
                elif is_miss:
                    msg = random.choice(["che cesso", "paracarro", "imbarazzante"])
                else:
                    msg = random.choice(["vabbè", "imbarazzanti", "ciao"])

            cleaned = validate_and_clean(msg, pid, p["max_words"])
            results.append({
                "persona_id": pid,
                "persona_name": p["name"],
                "delay_seconds": delay,
                "message": cleaned
            })

        # Sort by simulated arrival time
        results.sort(key=lambda x: x["delay_seconds"])
        return results
