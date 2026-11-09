import random
import re
from .personas import PERSONAS
from .validators import validate_and_clean
from .channel_parser import ChannelPostParser

# Matrice combinatoria base ad alta entropia (3.2M+ permutazioni)
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
        self.parser = ChannelPostParser()

    def get_delays(self):
        delays = {}
        for pid, pdata in self.personas.items():
            low, high = pdata["delay_range"]
            delays[pid] = random.randint(low, high)
        return delays

    def _generate_slot_message(self, persona_id, ptype, meta):
        """Generatore combinatorio dinamico basato sul contesto del post."""
        scorer = meta.get("scorer") or "lui"
        assister = meta.get("assister")
        team_home = meta.get("team_home") or "squadra"
        team_away = meta.get("team_away") or "avversari"
        player = meta.get("player") or scorer

        if ptype == "GOAL":
            if persona_id == 1:  # Emotivo
                excl = random.choice(["SEEEEEEE", "MAMMA MIA", "GODOOOO", "INUMANO", "NON CI CREDO", "DAI CAZZO"])
                praise = random.choice([
                    f"CHE GOL DI {scorer.upper()}",
                    f"{scorer.upper()} SEI UN FENOMENO",
                    f"DISTRUGGILI TUTTI {scorer.upper()}",
                    f"GOL ASSURDO DI {scorer.upper()}",
                    f"{scorer.upper()} MAMMA MIA CHE GIOCATA"
                ])
                tail = random.choice(["SEEEE", "GODO TROPPO", "NON CI CREDO MAI", "MUTI TUTTI", "SPETTACOLO"])
                return f"{excl} {praise} {tail}"

            elif persona_id == 2:  # Cinico
                prefix = random.choice(["comunque", "tanto", "solita botta di culo", "ovvio che", "difesa che"])
                team_target = team_away.lower() if random.random() < 0.6 else team_home.lower()
                subj = random.choice([f"la difesa del {team_target}", f"{scorer.lower()}", "il portiere", "il centrale"])
                act = random.choice(["dorme in piedi", "trova un rimpallo fortunato", "segna a porta vuota", "fa una papera"])
                close = random.choice(["come al solito", "tanto mo pareggiano", "partita orrenda comunque", "da serie c", "ridicolo davvero"])
                return f"{prefix} {subj} {act} {close}"

            elif persona_id == 3:  # Troll
                subj = scorer.lower()
                target_team = team_away.lower()
                mock = random.choice([
                    f"{subj} gli esulta pure in faccia",
                    f"tifosi del {target_team} già a piangere sotto la doccia",
                    f"{subj} li manda tutti a dormire",
                    f"manco con le mani la prendevano",
                    f"difesa del {target_team} a farfalle"
                ])
                laugh = random.choice(["ahahahah", "ahahah piango", "ahahah godo", "ahahah muti"])
                return f"{mock} {laugh}"

            elif persona_id == 4:  # Fanta
                if assister:
                    opts = [
                        f"assist confermato a {assister.lower()} o lo tolgono?",
                        f"ho {scorer.lower()} al fanta godoooo",
                        f"assist di {assister.lower()} godo per il +1",
                        f"ovvio che mi segna contro {scorer.lower()} sto cane",
                        f"+3 di {scorer.lower()} e +1 di {assister.lower()} giornata salvata"
                    ]
                else:
                    opts = [
                        f"ovvio che mi segna contro {scorer.lower()} maledetto",
                        f"ce l'ho contro al fanta ovvio",
                        f"ho {scorer.lower()} al fanta godoooooo",
                        f"mi ha bruciato la schedina sto gol",
                        f"+3 di {scorer.lower()} dai che si vince la giornata"
                    ]
                return random.choice(opts)

            elif persona_id == 5:  # Telegrafico
                pool = [scorer.lower(), "godo", "meritato", "finita", "solito culo", "golazo", "fenomeno"]
                return random.choice(pool)

        elif ptype == "LINEUP":
            if persona_id == 1:
                return random.choice(["DAI RAGAZZI CARICHI FORZA", "FORMAZIONE TOP SI VINCE", "MAMMA MIA CHE SQUADRA CARICHI"])
            elif persona_id == 2:
                prefix = random.choice(["comunque", "tanto", "solita storia"])
                act = random.choice(["formazione oscena", "scelte senza senso del mister", "con sti titolari non si va da nessuna parte"])
                close = random.choice(["prevedo disastri", "come al solito", "solito scempio"])
                return f"{prefix} {act} {close}"
            elif persona_id == 3:
                return random.choice(["ancora titolare sto cesso ahahah", "questi stasera ne prendono quattro ahahah", "in panchina a piangere ahahah"])
            elif persona_id == 4:
                return random.choice(["chi avete titolare al fanta?", "messo in panchina sto cane maledetto", "ballottaggio perso al fanta ovvio"])
            elif persona_id == 5:
                return random.choice(["disastro", "vittoria facile", "vabbè"])

        elif ptype == "INJURY":
            if persona_id == 1:
                return random.choice([f"NOOO CHE BRUTTO INFORTUNIO PER {player.upper()}", "SPERIAMO NIENTE DI GRAVE MAMMA MIA", "STAGIONE FINITA CHE SFIGA ASSURDA"])
            elif persona_id == 2:
                return random.choice([f"stagione compromessa per {player.lower()} preparatori da cacciare", "solita sfiga che si ripete sempre", "preparazione atletica da serie c"])
            elif persona_id == 3:
                return random.choice([f"fatto di cristallo {player.lower()} ahahah", "nemmeno tre partite di fila regge ahahah", "in infermeria fisso ormai"])
            elif persona_id == 4:
                return random.choice([f"fanta distrutto per l'infortunio di {player.lower()}", "svincolo obbligatorio all'asta di riparazione", "avevo investito mezzo budget su di lui"])
            elif persona_id == 5:
                return random.choice(["rotto", "sfiga", "stagione finita"])

        elif ptype == "FULL_TIME":
            if persona_id == 1:
                return random.choice(["FINITAAAAA GODOOO CHE PARTITA", "SEEE VITTORIA MERITATA RAGAZZI", "CHE SCHIFO DI PARTITA NON CI CREDO"])
            elif persona_id == 2:
                return random.choice(["partita orrenda comunque vinta solo a culo", "tanto non andranno mai da nessuna parte", "zero gioco solita prestazione ridicola"])
            elif persona_id == 3:
                return random.choice(["tutti a casa e a nanna adesso dai ahahah", "tifosi muti stasera ahahahah", "pagliacci totali a casa"])
            elif persona_id == 4:
                return random.choice(["giornata di fanta chiusa con una sconfitta", "schedina saltata per questa partita", "al fanta ho perso di mezzo punto"])
            elif persona_id == 5:
                return random.choice(["finita", "meritato", "scempio"])

        elif ptype == "HALF_TIME":
            if persona_id == 1:
                return random.choice(["SVEGLIATEVI NEL SECONDO TEMPO DAI", "MAMMA MIA CHE PRIMO TEMPO"])
            elif persona_id == 2:
                return random.choice(["primo tempo orrendo comunque zero tiri", "partita da addormentarsi proprio"])
            elif persona_id == 3:
                return random.choice(["che partitaccia oscena ahahah", "manco nei dilettanti ahahah"])
            elif persona_id == 4:
                return random.choice(["zero bonus in questo primo tempo", "speriamo nei cambi per il fanta"])
            elif persona_id == 5:
                return random.choice(["dormono", "orrendo", "vabbè"])

        elif ptype == "RED_CARD":
            if persona_id == 1:
                return random.choice(["MA CHE ROSSO È QUESTO DAI", "MA SEI PAZZO ARBITRO VENDUTO"])
            elif persona_id == 2:
                return random.choice(["in dieci finita la partita comunque", "fallo stupido e ingenuo giocatore senza cervello"])
            elif persona_id == 3:
                return random.choice(["interventi da galera ahahah", "ha cercato di decapitarlo ahahahah"])
            elif persona_id == 4:
                return random.choice(["rosso al fanta giornata rovinata subito", "-1 e addio vittoria al fanta"])
            elif persona_id == 5:
                return random.choice(["macellaio", "follia", "venduto"])

        elif ptype == "DISALLOWED":
            if persona_id == 1:
                return random.choice(["LADRI CLAMOROSI NON CI CREDO", "GODO ANNULLATO SEEE"])
            elif persona_id == 2:
                return random.choice(["fuorigioco di un millimetro solita farsa", "tanto con questo var non si capisce niente"])
            elif persona_id == 3:
                return random.choice(["il var colpisce ancora ahahahah goduria", "già avevano esultato ahahah che pagliacci"])
            elif persona_id == 4:
                return random.choice(["mi hanno tolto il bonus al fanta ladri", "schedina saltata per un millimetro"])
            elif persona_id == 5:
                return random.choice(["farsa", "annullato", "ladri"])

        else:  # Generico / Combinatoria aperta
            if persona_id == 1:
                return random.choice(["NON CI CREDO MA CHE ROBA È", "MAMMA MIA ASSURDO", "MA ANDATE A CAGARE DAI"])
            elif persona_id == 2:
                p = random.choice(PREFIXES)
                s = random.choice(SUBJECTS)
                a = random.choice(ACTIONS)
                c = random.choice(CLOSINGS)
                return f"{p} {s} {a} {c}"
            elif persona_id == 3:
                return random.choice(["ma chi cazzo sono questi ahahah", "pagliacci totali ahahahah", "e dove vogliono andare ahahah"])
            elif persona_id == 4:
                return random.choice(["fantacalcio distrutto per colpa di ste notizie", "chissà quanto prende al fanta questo"])
            elif persona_id == 5:
                return random.choice(TELEGRAFICI_POOL)

    def simulate_mock_reactions(self, post_text):
        """Genera le reazioni dei 5 archetipi al post del canale con delay temporali."""
        meta = self.parser.parse(post_text)
        ptype = meta["type"]

        delays = self.get_delays()
        results = []

        for pid in sorted(self.personas.keys()):
            p = self.personas[pid]
            delay = delays[pid]

            raw_msg = self._generate_slot_message(pid, ptype, meta)
            cleaned = validate_and_clean(raw_msg, pid, p["max_words"])

            results.append({
                "persona_id": pid,
                "persona_name": p["name"],
                "delay_seconds": delay,
                "message": cleaned
            })

        results.sort(key=lambda x: x["delay_seconds"])
        return results

    def simulate_thread(self, post_text, max_replies=3):
        """Simula una discussione a catena (multi-turno) in cui le personas si rispondono a vicenda sotto il post."""
        meta = self.parser.parse(post_text)
        ptype = meta["type"]

        # Seleziona persona per il commento genitore (spesso Emotivo, Cinico o Fanta)
        parent_pid = random.choice([1, 2, 4])
        parent_persona = self.personas[parent_pid]
        parent_delay = random.randint(parent_persona["delay_range"][0], parent_persona["delay_range"][1])

        parent_msg_raw = self._generate_slot_message(parent_pid, ptype, meta)
        parent_msg = validate_and_clean(parent_msg_raw, parent_pid, parent_persona["max_words"])

        thread = [
            {
                "id": 1,
                "in_reply_to_id": None,
                "persona_id": parent_pid,
                "persona_name": parent_persona["name"],
                "delay_seconds": parent_delay,
                "message": parent_msg
            }
        ]

        # Template di risposta bot-to-bot calibrati sulla persona a cui si risponde
        def get_reply(responder_id, target_pid):
            if target_pid == 1:  # Risposta all'Emotivo
                if responder_id == 2:  # Cinico
                    return random.choice(["ma che urli che tanto la perdono al 90'", "calmati che han fatto un tiro in 80 minuti", "solito esaltato per un gol a caso"])
                elif responder_id == 3:  # Troll
                    return random.choice(["ahahahah sta già esultando piango", "ti sento piangere da qua ahahahah", "manco hanno vinto e fa il fenomeno"])
                elif responder_id == 4:  # Fanta
                    return random.choice(["urla pure intanto a me ha rovinato il fanta", "beato te io sto sotto di tre punti"])
                else:
                    return random.choice(["calmati", "esaltato", "vabbè"])

            elif target_pid == 2:  # Risposta al Cinico
                if responder_id == 1:  # Emotivo
                    return random.choice(["MA STAI ZITTO GUFO MALEDETTO", "MA GODITI LA PARTITA OGNI TANTO", "SEMPRE A PIANGERE MAI CONTENTO"])
                elif responder_id == 3:  # Troll
                    return random.choice(["il gufo supremo ha parlato ahahah", "comprati un maalox dai ahahahah", "ancora che parla questo ahahah"])
                elif responder_id == 4:  # Fanta
                    return random.choice(["ha ragione comunque al fanta mi ha distrutto", "per una volta concordo con te"])
                else:
                    return random.choice(["gufo", "taci", "rosica"])

            elif target_pid == 4:  # Risposta al Fanta
                if responder_id == 1:  # Emotivo
                    return random.choice(["MA PENSA ALLA SQUADRA VERA NON AL FANTA", "NON CE NE FREGA NIENTE DEL FANTA"])
                elif responder_id == 2:  # Cinico
                    return random.choice(["tanto la perdevi comunque la giornata", "già tanto che non hai preso -3"])
                elif responder_id == 3:  # Troll
                    return random.choice(["godo ahahahah chiudi l'app", "ma chi se ne frega del tuo fanta ahahah", "piangi ancora per il fantacalcio dai"])
                else:
                    return random.choice(["piangi", "spiace", "ciao fanta"])

            else:  # Risposta generica o al Troll
                if responder_id == 1:
                    return random.choice(["MA CHE RIDI COGLIONE", "PAGLIACCIO PENSA AI TUOI", "RIDI RIDI CHE DOMENICA TOCCA A TE"])
                elif responder_id == 2:
                    return random.choice(["ridi pure intanto siamo ridicoli", "fai poco lo spiritoso che il livello è questo"])
                elif responder_id == 3:
                    return random.choice(["e si gode ancora di più ahahah", "pagliaccio muto ahahah"])
                else:
                    return random.choice(["muti", "pagliaccio", "spariti"])

        available_responders = [pid for pid in [1, 2, 3, 4, 5] if pid != parent_pid]
        random.shuffle(available_responders)

        current_time = parent_delay
        last_id = 1

        for i in range(min(max_replies, len(available_responders))):
            resp_pid = available_responders[i]
            resp_persona = self.personas[resp_pid]
            delta = random.randint(8, 25)
            current_time += delta

            # Risponde o al messaggio originale (50%) o all'ultimo messaggio della conversazione (50%)
            target_msg = thread[0] if (random.random() < 0.5 or len(thread) == 1) else thread[-1]
            raw_reply = get_reply(resp_pid, target_msg["persona_id"])
            cleaned_reply = validate_and_clean(raw_reply, resp_pid, resp_persona["max_words"])

            new_id = last_id + 1
            thread.append({
                "id": new_id,
                "in_reply_to_id": target_msg["id"],
                "in_reply_to_persona": target_msg["persona_name"],
                "persona_id": resp_pid,
                "persona_name": resp_persona["name"],
                "delay_seconds": current_time,
                "message": cleaned_reply
            })
            last_id = new_id

        return thread
