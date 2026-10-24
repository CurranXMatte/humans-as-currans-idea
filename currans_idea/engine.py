import random
from .personas import PERSONAS
from .validators import validate_and_clean

# matrice combinatoria ad alta entropia: oltre 3.200.000 combinazioni uniche possibili
PREFIXES = [
    "comunque", "tanto", "vabbè ma", "ma come si fa", "solita storia", "nemmeno nei dilettanti",
    "non ci credo", "guardali", "non esaltatevi che", "pazzesco", "solita farsa", "arbitro comprato",
    "incredibile come", "madonna santa", "che schifo", "meritato", "godo troppo", "manco quotato",
    "telefonato proprio", "ennesimo regalo", "vergognosi tutti", "ridicoli come sempre", "mamma mia che",
    "partita venduta", "solito furto", "difesa che", "mister che", "partita orrenda", "il var che",
    "ennesima papera", "scandalo totale", "ma andate a cagare", "che giocatore osceno", "che perla",
    "ma dove vogliono andare", "ovvio che", "solita botta di culo", "stagione già finita", "follia totale", "senza parole"
]

SUBJECTS = [
    "la difesa", "il portiere", "l'arbitro", "il mister", "la punta", "il terzino", "il centrale",
    "il var", "la curva", "la squadra", "il guardalinee", "il capitano", "il centrocampo", "la panchina",
    "lautaro", "leao", "vlahovic", "orsolini", "lukaku", "dybala", "kvara", "lookman", "kean",
    "zapata", "barella", "calhanoglu", "theo", "gatti", "bremer", "sommer", "maignan", "carnesecchi",
    "morata", "retegui", "pulisic", "zaccagni", "castellanos", "thuram", "allegri", "conte", "motta"
]

ACTIONS = [
    "fa una papera", "dorme in piedi", "si fa cacciare", "segna a porta vuota", "regala un rigore",
    "tira sulla luna", "fa un fallo da galera", "sbaglia lo stop", "non azzecca un passaggio",
    "cade da solo", "chiede il cambio", "salva sulla linea", "la butta dentro", "esulta in faccia",
    "piange con l'arbitro", "prende il palo", "inventa una giocata", "non corre manco", "si fa saltare",
    "perde palla da pollo", "regala l'angolo", "segna il gol dell'ex", "para pure le mosche",
    "subisce fallo netto", "non vede un fuorigioco", "fischia a senso unico", "sbaglia clamorosamente",
    "trova il gol della domenica", "sfiora l'incrocio", "manda la palla in curva", "liscia il pallone",
    "provoca la rissa", "si mangia un gol fatto", "salta l'uomo facile", "fa un assist perfetto",
    "protesta per niente", "esce a vuoto", "devia nella propria porta", "trova un rimpallo fortunato", "fa il fenomeno"
]

CLOSINGS = [
    "come al solito", "senza vergogna", "manco su fifa", "da serie c", "ridicolo davvero",
    "vaffanculo va", "ahahah piango", "che goduria immensa", "da cacciare a calci", "pagliacci totali",
    "non ci credo mai", "giornata finita", "tanto retrocedono", "manco con le mani", "ahahah che scempio",
    "ho perso la bolla", "stagione finita", "allucinante", "solita vergogna", "pure con presunzione",
    "zero dignità", "e tutti zitti", "da ufficio inchieste", "meritatissimo dai", "incredibile davvero",
    "manco nei sogni", "a porta spalancata", "da galera pura", "ahahah muti tutti", "da non crederci",
    "e stiamo a guardare", "solito scandalo", "ma per favore", "farsa autentica", "mai vista una roba così",
    "e si gode", "imbarazzo totale", "non ho parole", "spettacolo puro", "sempre la stessa storia"
]

TELEGRAFICI_POOL = [
    "godo", "meritato", "che cesso", "paracarro", "finita", "imbarazzante",
    "farsa", "papera", "ladri", "macellaio", "vabbè", "ciao", "scandalo",
    "vergogna", "peccato", "muti", "piango", "tragicomico", "bidone",
    "colpaccio", "strapagato", "tardi", "era ora", "sfiga", "rotto",
    "rigore netto", "fallo netto", "fuorigioco netto", "rosso netto",
    "solito culo", "goduria totale", "che schifo", "che partitaccia",
    "parata assurda", "imbarazzanti", "ridicoli", "capolavoro", "disastro",
    "spettacolo", "senza parole", "annullato", "venduto", "fenomeno"
]

class CurransIdeaEngine:
    def __init__(self, personas_config=None):
        self.personas = personas_config or PERSONAS

    def get_delays(self):
        delays = {}
        for pid, pdata in self.personas.items():
            low, high = pdata["delay_range"]
            delays[pid] = random.randint(low, high)
        return delays

    def detect_category(self, event_lower):
        if any(w in event_lower for w in ["annullat", "fuorigioco", "gol tolto", "var annulla"]):
            return "disallowed_goal"
        if any(w in event_lower for w in ["autogol", "deviazione sfortunata"]):
            return "own_goal"
        if any(w in event_lower for w in ["sbagliat", "parato", "fallito", "palo rigore"]):
            return "missed_penalty"
        if any(w in event_lower for w in ["rosso", "espuls", "in 10", "doppio giallo"]):
            return "red_card"
        if any(w in event_lower for w in ["infortun", "crociato", "barella", "lesione"]):
            return "injury"
        if any(w in event_lower for w in ["esoner", "cacciato l'allenatore", "dimissioni"]):
            return "sacking"
        if any(w in event_lower for w in ["mercato", "ufficiale", "trattativa", "acquistat", "cedut", "firmato"]):
            return "transfer_market"
        if any(w in event_lower for w in ["gol", "rete", "vantaggio", "segna", "ribalta", "raddoppio"]):
            return "goal"
        return "general"

    def generate_unique_synthetic_message(self, persona_id, index=None):
        # genera varianti dinamiche scalabili a oltre 500k messaggi unici
        p = self.personas[persona_id]
        
        if persona_id == 5:
            msg = random.choice(TELEGRAFICI_POOL)
            return validate_and_clean(msg, persona_id, p["max_words"])
            
        if index is not None:
            c_idx = index % len(CLOSINGS)
            a_idx = (index // len(CLOSINGS)) % len(ACTIONS)
            s_idx = (index // (len(CLOSINGS) * len(ACTIONS))) % len(SUBJECTS)
            p_idx = (index // (len(CLOSINGS) * len(ACTIONS) * len(SUBJECTS))) % len(PREFIXES)
            base = f"{PREFIXES[p_idx]} {SUBJECTS[s_idx]} {ACTIONS[a_idx]} {CLOSINGS[c_idx]}"
        else:
            base = f"{random.choice(PREFIXES)} {random.choice(SUBJECTS)} {random.choice(ACTIONS)} {random.choice(CLOSINGS)}"

        if persona_id == 1: # Emotivo: caps lock parziale e stringa corta
            words = base.split()
            msg = " ".join(words[:4]).upper()
        elif persona_id == 2: # Cinico: lowercase
            words = base.split()
            msg = " ".join(words[:6]).lower()
        elif persona_id == 3: # Troll: sfottò con risata
            words = base.split()
            msg = f"{' '.join(words[:5])} ahahah"
        elif persona_id == 4: # Fanta: attacco fanta
            words = base.split()
            msg = f"al fanta {' '.join(words[:6])}"
            
        return validate_and_clean(msg, persona_id, p["max_words"])

    def simulate_mock_reactions(self, event_text):
        event_lower = event_text.lower()
        delays = self.get_delays()
        results = []
        cat = self.detect_category(event_lower)

        for pid in sorted(self.personas.keys()):
            p = self.personas[pid]
            delay = delays[pid]

            if pid == 1:
                if cat == "goal":
                    msg = random.choice(["SEEEEEEE PROPRIO LUI GODOOO", "MAMMA MIA CHE SQUADRA SEEE", "GODOOOO FINALMENTE", "CHE CAZZO DI GOL MAMMA MIA", "GODOOOOOOOOO"])
                elif cat == "disallowed_goal":
                    msg = random.choice(["NON CI CREDO MA CHE FURTO DAI", "GODO ANNULLATO SEEE", "MA QUALE FUORIGIOCO MA DAI", "LADRI CLAMOROSI NON CI CREDO"])
                elif cat == "own_goal":
                    msg = random.choice(["NON CI CREDO CHE PAPERA ASSURDA", "MA COME SI FA UN AUTOGOL COSÌ", "MAMMA MIA CHE SFIGA"])
                elif cat == "missed_penalty":
                    msg = random.choice(["NON CI CREDO MA COME SI FA DAI", "MA VAI A CAGARE VA", "IN POZZO SENZA FONDO NON CI CREDO", "MA COME CAZZO L'HA TIRATO"])
                elif cat == "red_card":
                    msg = random.choice(["MA CHE ROSSO È QUESTO DAI", "MA SEI PAZZO ARBITRO VENDUTO", "FALLO DA ASSASSINO GIUSTO IL ROSSO"])
                elif cat == "injury":
                    msg = random.choice(["NOOO CHE BRUTTO INFORTUNIO CAZZO", "SPERIAMO NIENTE DI GRAVE MAMMA MIA", "STAGIONE FINITA CHE SFIGA"])
                elif cat == "sacking":
                    msg = random.choice(["FINALMENTE CACCIATO DIO MIO", "ERA ORA NON NE POTEVO PIÙ", "VERGOGNA SOCIETÀ RIDICOLA"])
                elif cat == "transfer_market":
                    msg = random.choice(["MAMMA MIA CHE COLPO ASSURDO", "BENVENUTO CAMPIONE FINALMENTE", "SOLDI BUTTATI NEL CESSO"])
                else:
                    msg = random.choice(["NON CI CREDO", "MAMMA MIA", "MA CHE ROBA È"])

            elif pid == 2:
                if cat == "goal":
                    msg = random.choice(["difesa imbarazzante comunque dormivano tutti", "partita orrenda comunque vinta solo a culo", "tanto so già come va a finire", "non esaltatevi che fan cagare entrambi", "tanto mo pareggiano sicuro come al solito"])
                elif cat == "disallowed_goal":
                    msg = random.choice(["tanto con questo var non si capisce più niente", "fuorigioco di un millimetro solita farsa", "arbitro completamente in confusione"])
                elif cat == "own_goal":
                    msg = random.choice(["difensore da serie c comunque imbarazzante", "gol tragicomico degno di questa squadra", "difesa che manco nei dilettanti fa ste robe"])
                elif cat == "missed_penalty":
                    msg = random.choice(["rigore osceno comunque giocatore pippissimo", "paracarro inutile come sempre", "non segna manco a porta vuota questo", "che cesso di giocatore comunque"])
                elif cat == "red_card":
                    msg = random.choice(["in dieci finita la partita comunque", "fallo stupido e ingenuo giocatore senza cervello", "arbitro protagonista come sempre una vergogna"])
                elif cat == "injury":
                    msg = random.choice(["stagione finita sicuro crociato andato", "preparatori atletici da cacciare comunque", "solita sfiga che si ripete"])
                elif cat == "sacking":
                    msg = random.choice(["tanto chiunque mettono in panchina fallisce", "esonero tardivo stagione già compromessa", "la colpa è della dirigenza non del mister"])
                elif cat == "transfer_market":
                    msg = random.choice(["giocatore sopravvalutato e stipendio spropositato", "soldi spesi malissimo comunque non serve a niente", "ennesimo bidone preso dalla dirigenza"])
                else:
                    msg = random.choice(["comunque una partita orrenda", "arbitro comprato sicuro come al solito", "il culo che hanno questi comunque clamoroso"])

            elif pid == 3:
                if cat == "goal":
                    msg = random.choice(["questo gli esulta pure in faccia godo ahahahah", "tutti zitti adesso dai pagliacci", "manco con le mani la prendeva ahahah", "staranno 3 mesi a piangere hahah"])
                elif cat == "disallowed_goal":
                    msg = random.choice(["il var colpisce ancora ahahahah goduria", "già avevano esultato ahahah che pagliacci", "linee tirate a caso col righello ahahah"])
                elif cat == "own_goal":
                    msg = random.choice(["autogol da mai dire gol ahahahah", "manco se ci provava 100 volte la metteva lì ahahah", "che papera clamorosa ahahahah"])
                elif cat == "missed_penalty":
                    msg = random.choice(["ma dove cazzo voleva tirarlo ahahahah", "pallone sulla luna ahahah", "ci riprova altre 10 volte va in curva ahahah", "manco con le mani segnano questi ahahah"])
                elif cat == "red_card":
                    msg = random.choice(["ha cercato di decapitarlo ahahahah", "rosso sacrosanto che macellaio ahahah", "interventi da galera ahahah"])
                elif cat == "injury":
                    msg = random.choice(["fatto di cristallo questo giocatore ahahah", "nemmeno tre partite di fila regge", "in infermeria fisso ormai"])
                elif cat == "sacking":
                    msg = random.choice(["il pelato già a spasso ahahahah", "hanno chiamato mazzarri ahahahah", "tragicommedia finita finalmente"])
                elif cat == "transfer_market":
                    msg = random.choice(["questo a gennaio è già in prestito ahahah", "50 milioni per uno scaldabagno ahahah", "affare del secolo per chi l'ha venduto ahahah"])
                else:
                    msg = random.choice(["ma chi cazzo è questo ahahah", "pagliacci totali ahahahah", "e dove va ahahah"])

            elif pid == 4:
                if cat == "goal":
                    msg = random.choice(["ovvio che mi segna contro al fanta sto maledetto", "assist confermato o l'hanno tolto?", "ce l'ho contro porco dio", "scamacca contro al fanta godoooooo"])
                elif cat == "disallowed_goal":
                    msg = random.choice(["mi hanno tolto il bonus al fanta ladri", "avevo il suo gol al fanta bastardi", "schedina saltata per un millimetro"])
                elif cat == "own_goal":
                    msg = random.choice(["malus autogol al fanta dio cane", "il mio difensore che fa autogol ovvio", "-2 al fanta per sto scempio"])
                elif cat == "missed_penalty":
                    msg = random.choice(["ovvio mi ha bruciato la schedina sto cane", "messo titolare al fanta per sto -3", "ho perso la bolla per colpa sua"])
                elif cat == "red_card":
                    msg = random.choice(["rosso al fanta giornata rovinata subito", "gioco in 10 al fanta vaffanculo", "-1 e addio vittoria al fanta"])
                elif cat == "injury":
                    msg = random.choice(["avevo investito mezzo budget su di lui al fanta", "fanta distrutto per l'infortunio ciao", "svincolo obbligatorio all'asta di riparazione"])
                elif cat == "sacking":
                    msg = random.choice(["ora cambiano tutti i titolari al fanta", "addio ai miei pupilli che giocavano con lui", "vediamo chi mette titolare il nuovo mister"])
                elif cat == "transfer_market":
                    msg = random.choice(["all'asta del fanta andrà a ruba", "prezzo folle al fanta non lo prendo mai", "da prendere subito all'asta"])
                else:
                    msg = random.choice(["fantacalcio distrutto per colpa sua", "quanto prende secondo voi?", "mi ha fatto saltare la schedina"])

            elif pid == 5:
                if cat == "goal":
                    msg = random.choice(["godo", "meritato", "finita"])
                elif cat == "disallowed_goal":
                    msg = random.choice(["farsa", "annullato", "godo", "ladri"])
                elif cat == "own_goal":
                    msg = random.choice(["papera", "imbarazzante", "tragicomico"])
                elif cat == "missed_penalty":
                    msg = random.choice(["che cesso", "paracarro", "imbarazzante"])
                elif cat == "red_card":
                    msg = random.choice(["macellaio", "follia", "finita", "venduto"])
                elif cat == "injury":
                    msg = random.choice(["rotto", "sfiga", "finita"])
                elif cat == "sacking":
                    msg = random.choice(["esonerato", "era ora", "tardi"])
                elif cat == "transfer_market":
                    msg = random.choice(["bidone", "colpaccio", "inutile", "strapagato"])
                else:
                    msg = random.choice(["vabbè", "imbarazzante", "ciao"])

            cleaned = validate_and_clean(msg, pid, p["max_words"])
            results.append({
                "persona_id": pid,
                "persona_name": p["name"],
                "delay_seconds": delay,
                "message": cleaned
            })

        results.sort(key=lambda x: x["delay_seconds"])
        return results
