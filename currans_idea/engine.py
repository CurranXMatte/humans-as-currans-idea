import random
from .personas import PERSONAS
from .validators import validate_and_clean

# da committare dopo il test
class CurransIdeaEngine:
    def __init__(self, personas_config=None):
        self.personas = personas_config or PERSONAS

    def get_delays(self):
        # delay randomici per simulare umani che scrivono
        delays = {}
        for pid, pdata in self.personas.items():
            low, high = pdata["delay_range"]
            delays[pid] = random.randint(low, high)
        return delays

    def format_prompt_for_llm(self, event_text, persona_id):
        # prompt per le chiamate future via api
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

    def simulate_mock_reactions(self, event_text):
        # test simulazione locale
        event_lower = event_text.lower()
        delays = self.get_delays()
        results = []

        # check base parole chiave
        is_goal = "gol" in event_lower or "rete" in event_lower
        is_miss = "sbagliato" in event_lower or "errore" in event_lower or "palo" in event_lower or "fuori" in event_lower
        is_card = "rosso" in event_lower or "espulso" in event_lower or "giallo" in event_lower

        for pid in sorted(self.personas.keys()):
            p = self.personas[pid]
            delay = delays[pid]

            if pid == 1:
                if is_goal:
                    msg = random.choice(["SEEEEEEE PROPRIO LUI GODOOO", "MAMMA MIA CHE GIOCATORE SEEE", "GODOOOO FINALMENTE"])
                elif is_miss:
                    msg = random.choice(["NON CI CREDO MA COME SI FA DAI", "MA VAI A CAGARE VA", "IN POZZO SENZA FONDO NON CI CREDO"])
                else:
                    msg = random.choice(["NON CI CREDO", "MAMMA MIA", "MA CHE ROBA È"])

            elif pid == 2:
                if is_goal:
                    msg = random.choice(["difesa imbarazzante comunque dormivano tutti", "gol a culo tanto mo pareggiano", "non esaltatevi che fan cagare entrambi"])
                elif is_miss:
                    msg = random.choice(["rigore osceno comunque giocatore pippissimo", "paracarro inutile come sempre", "non segna manco a porta vuota questo"])
                else:
                    msg = random.choice(["partita oscena comunque", "arbitro comprato sicuro"])

            elif pid == 3:
                if is_goal:
                    msg = random.choice(["questo gli esulta pure in faccia godo ahahahah", "tutti zitti adesso dai", "manco con le mani la prendeva ahahah"])
                elif is_miss:
                    msg = random.choice(["ma dove cazzo voleva tirarlo ahahahah", "pallone sulla luna ahahah", "nemmeno su fifa uno scempio simile"])
                else:
                    msg = random.choice(["ma chi cazzo è questo ahahah", "pagliacci totali"])

            elif pid == 4:
                if is_goal:
                    msg = random.choice(["ovvio che mi segna contro al fanta sto maledetto", "assist confermato o l'hanno tolto?", "ce l'ho contro porco dio"])
                elif is_miss:
                    msg = random.choice(["ovvio mi ha bruciato la schedina sto cane", "messo titolare al fanta per sto -3", "ho perso la bolla per colpa sua"])
                else:
                    msg = random.choice(["fantacalcio distrutto per colpa sua", "quanto prende secondo voi?"])

            elif pid == 5:
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

        # ordino per tempo di invio
        results.sort(key=lambda x: x["delay_seconds"])
        return results
