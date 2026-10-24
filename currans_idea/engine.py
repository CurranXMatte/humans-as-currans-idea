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
        # test simulazione locale con campioni appresi dai 45.5k messaggi
        event_lower = event_text.lower()
        delays = self.get_delays()
        results = []

        is_goal = any(w in event_lower for w in ["gol", "rete", "vantaggio", "segnato"])
        is_miss = any(w in event_lower for w in ["sbagliato", "errore", "palo", "fuori", "parato"])
        is_card = any(w in event_lower for w in ["rosso", "espulso", "giallo", "fallo", "var"])

        for pid in sorted(self.personas.keys()):
            p = self.personas[pid]
            delay = delays[pid]

            if pid == 1:
                if is_goal:
                    msg = random.choice([
                        "SEEEEEEE PROPRIO LUI GODOOO",
                        "MAMMA MIA CHE SQUADRA SEEE",
                        "GODOOOO FINALMENTE",
                        "CHE CAZZO DI GOL MAMMA MIA",
                        "GODOOOOOOOOO"
                    ])
                elif is_miss:
                    msg = random.choice([
                        "NON CI CREDO MA COME SI FA DAI",
                        "MA VAI A CAGARE VA",
                        "IN POZZO SENZA FONDO NON CI CREDO",
                        "MA COME CAZZO L'HA TIRATO"
                    ])
                else:
                    msg = random.choice([
                        "NON CI CREDO",
                        "MAMMA MIA",
                        "MA CHE ROBA È"
                    ])

            elif pid == 2:
                if is_goal:
                    msg = random.choice([
                        "difesa imbarazzante comunque dormivano tutti",
                        "partita orrenda comunque vinta solo a culo",
                        "tanto so già come va a finire",
                        "non esaltatevi che fan cagare entrambi",
                        "tanto mo pareggiano sicuro come al solito"
                    ])
                elif is_miss:
                    msg = random.choice([
                        "rigore osceno comunque giocatore pippissimo",
                        "paracarro inutile come sempre",
                        "non segna manco a porta vuota questo",
                        "che cesso di giocatore comunque"
                    ])
                else:
                    msg = random.choice([
                        "comunque una partita orrenda",
                        "arbitro comprato sicuro come al solito",
                        "il culo che hanno questi comunque clamoroso"
                    ])

            elif pid == 3:
                if is_goal:
                    msg = random.choice([
                        "questo gli esulta pure in faccia godo ahahahah",
                        "tutti zitti adesso dai pagliacci",
                        "manco con le mani la prendeva ahahah",
                        "staranno 3 mesi a piangere hahah"
                    ])
                elif is_miss:
                    msg = random.choice([
                        "ma dove cazzo voleva tirarlo ahahahah",
                        "pallone sulla luna ahahah",
                        "ci riprova altre 10 volte va in curva ahahah",
                        "manco con le mani segnano questi ahahah"
                    ])
                else:
                    msg = random.choice([
                        "ma chi cazzo è questo ahahah",
                        "pagliacci totali ahahahah",
                        "e dove va ahahah"
                    ])

            elif pid == 4:
                if is_goal:
                    msg = random.choice([
                        "ovvio che mi segna contro al fanta sto maledetto",
                        "assist confermato o l'hanno tolto?",
                        "ce l'ho contro porco dio",
                        "scamacca contro al fanta godoooooo"
                    ])
                elif is_miss:
                    msg = random.choice([
                        "ovvio mi ha bruciato la schedina sto cane",
                        "messo titolare al fanta per sto -3",
                        "ho perso la bolla per colpa sua"
                    ])
                else:
                    msg = random.choice([
                        "fantacalcio distrutto per colpa sua",
                        "quanto prende secondo voi?",
                        "mi ha fatto saltare la schedina"
                    ])

            elif pid == 5:
                if is_goal:
                    msg = random.choice(["godo", "meritato", "finita"])
                elif is_miss:
                    msg = random.choice(["che cesso", "paracarro", "imbarazzante"])
                else:
                    msg = random.choice(["vabbè", "imbarazzante", "ciao"])

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
