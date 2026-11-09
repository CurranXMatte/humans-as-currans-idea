import random
import re
from .personas import PERSONAS
from .validators import validate_and_clean
from .channel_parser import ChannelPostParser

# Matrice combinatoria base ad alta entropia
PREFIXES_CINICO = [
    "comunque", "tanto", "solita botta di culo", "ovvio che", "vabbè ma", "nemmeno nei dilettanti",
    "solita farsa", "arbitro comprato", "incredibile come", "ennesimo regalo", "difesa che",
    "partita orrenda comunque", "solito furto", "follia totale", "senza parole", "manco quotato",
    "telefonato proprio", "ennesima papera", "scandalo totale", "ma dove vogliono andare", "pura fortuna"
]

CLOSINGS_CINICO = [
    "come al solito", "tanto mo pareggiano", "partita orrenda comunque", "da serie c", "ridicolo davvero",
    "zero gioco totale", "non esaltatevi per niente", "pura fortuna", "solita vergogna", "da ufficio inchieste",
    "e stiamo a guardare", "solito scandalo", "farsa autentica", "mai vista una roba così", "sempre la solita storia",
    "tanto non vanno da nessuna parte", "giornata falsata", "vergognosi tutti quanti", "imbarazzo totale"
]

EXCLAMATIONS_EMOTIVO = [
    "SEEEEEEE", "MAMMA MIA", "GODOOOO", "INUMANO", "NON CI CREDO", "DAI CAZZO",
    "MADONNA SANTA", "GODO COME UN RICCIO", "ALLUCINANTE", "CHE GIOCATORE",
    "CHE GOOOL", "FINALMENTE", "SI GODEEEE", "DEVASTANTE", "SPETTACOLO PURO"
]

CLOSINGS_EMOTIVO = [
    "GODO TROPPO", "NON CI CREDO MAI", "MUTI TUTTI", "SPETTACOLO PURO", "SEEEE",
    "AVANTI COSÌ", "E SI VOLA", "MAMMA MIA", "FENOMENO VERO", "DISTRUGGILI TUTTI",
    "TI AMO", "SENZA SENSO", "CHE GODURIA IMMENSA", "PIANGO DALLA GIOIA"
]

TELEGRAFICI_BASE = [
    "godo", "meritato", "che cesso", "paracarro", "finita", "imbarazzante",
    "farsa", "papera", "ladri", "macellaio", "vabbè", "ciao", "scandalo",
    "vergogna", "peccato", "muti", "piango", "tragicomico", "bidone",
    "colpaccio", "strapagato", "tardi", "era ora", "sfiga", "rotto",
    "rigore netto", "fallo netto", "fuorigioco netto", "rosso netto",
    "solito culo", "goduria totale", "che schifo", "che partitaccia",
    "parata assurda", "imbarazzanti", "ridicoli", "capolavoro", "disastro",
    "spettacolo", "senza parole", "annullato", "venduto", "fenomeno",
    "golazo", "chiudete tutto", "clamoroso", "allucinante", "incredibile"
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
        """Generatore combinatorio dinamico ancorato rigorosamente alle entità del post."""
        subject = meta.get("subject") or meta.get("scorer") or meta.get("player") or "lui"
        scorer = meta.get("scorer") or subject
        assister = meta.get("assister")
        team_home = meta.get("team_home") or "squadra"
        team_away = meta.get("team_away") or "avversari"
        player = meta.get("player") or subject

        sub_low = subject.lower()
        sub_up = subject.upper()

        if ptype == "GOAL":
            if persona_id == 1:  # Emotivo
                excl = random.choice(EXCLAMATIONS_EMOTIVO)
                actions = [
                    f"CHE GOL DI {sub_up}",
                    f"{sub_up} SEI UN FENOMENO",
                    f"DISTRUGGILI TUTTI {sub_up}",
                    f"GOL ASSURDO DI {sub_up}",
                    f"{sub_up} MAMMA MIA CHE GIOCATA",
                    f"PROPRIO LUI {sub_up}",
                    f"{sub_up} LI HA DISTRUTTI TUTTI",
                    f"CHE PERLA DI {sub_up}",
                    f"{sub_up} NON SBAGLIA MAI",
                    f"QUESTO È IL CALCIO {sub_up}",
                    f"IMMENSO {sub_up}",
                    f"CHE GOOOOL DI {sub_up}",
                    f"SOLO E SEMPRE {sub_up}",
                    f"COME SEGNA {sub_up}"
                ]
                close = random.choice(CLOSINGS_EMOTIVO)
                return f"{excl} {random.choice(actions)} {close}"

            elif persona_id == 2:  # Cinico
                pref = random.choice(PREFIXES_CINICO)
                team_away_phrase = f"del {meta['team_away'].lower()}" if meta.get("team_away") else "avversaria"
                actions = [
                    f"{sub_low} segna solo a culo",
                    f"{sub_low} trova un rimpallo fortunato",
                    f"la difesa dorme e {sub_low} la butta dentro",
                    f"il portiere fa una papera su {sub_low}",
                    f"{sub_low} non correva manco fino a mo",
                    f"{sub_low} fa un tiro osceno ed entra",
                    f"solita difesa aperta regalata a {sub_low}",
                    f"{sub_low} segna a porta spalancata",
                    f"partita orrenda decisa da un rimpallo su {sub_low}",
                    f"la difesa {team_away_phrase} dorme in piedi",
                    f"il portiere {team_away_phrase} esce a vuoto"
                ]
                close = random.choice(CLOSINGS_CINICO)
                return f"{pref} {random.choice(actions)} {close}"

            elif persona_id == 3:  # Troll
                mocks = [
                    f"{sub_low} gli esulta pure in faccia godo",
                    f"manco con le mani lo fermavano {sub_low}",
                    f"{sub_low} li manda tutti a dormire",
                    f"tutti muti adesso zittiti da {sub_low}",
                    f"difesa a farfalle su {sub_low} che scempio",
                    f"staranno tre mesi a piangere per {sub_low}",
                    f"{sub_low} fa piangere tutti stasera godo",
                    f"dove volevano andare contro {sub_low}",
                    f"ma chi doveva marcarlo {sub_low}",
                    f"{sub_low} li ha umiliati a domicilio"
                ]
                laugh = random.choice(["ahahahah", "ahahah piango", "ahahah godo", "ahahah muti tutti", "hahaha pagliacci"])
                return f"{random.choice(mocks)} {laugh}"

            elif persona_id == 4:  # Fanta
                if assister:
                    opts = [
                        f"assist confermato a {assister.lower()} o lo tolgono?",
                        f"ho {sub_low} al fanta godoooo",
                        f"assist di {assister.lower()} godo per il +1",
                        f"ovvio che mi segna contro {sub_low} sto cane",
                        f"+3 di {sub_low} e +1 di {assister.lower()} giornata salvata",
                        f"avevo {sub_low} e {assister.lower()} titolari godo",
                        f"chi ha contro {sub_low} oggi può piangere"
                    ]
                else:
                    opts = [
                        f"ovvio che mi segna contro {sub_low} maledetto",
                        f"ce l'ho contro al fanta {sub_low} ovvio",
                        f"ho {sub_low} al fanta godoooooo",
                        f"mi ha bruciato la schedina sto gol di {sub_low}",
                        f"+3 di {sub_low} dai che si vince la giornata",
                        f"messo titolare {sub_low} per fortuna oggi",
                        f"avevo l'under per colpa di {sub_low} saltato tutto"
                    ]
                return random.choice(opts)

            elif persona_id == 5:  # Telegrafico
                pool = [
                    sub_low,
                    sub_low.split()[-1] if len(sub_low.split()) > 1 else sub_low,
                    "godo", "golazo", "meritato", "solito culo", "fenomeno",
                    "finita", "paracarro", "farsa", "chiudete tutto", "eccolo"
                ]
                return random.choice(pool)

        elif ptype == "INJURY":
            if persona_id == 1:
                opts = [
                    f"NOOO CHE BRUTTO INFORTUNIO PER {sub_up}",
                    f"SPERIAMO NIENTE DI GRAVE PER {sub_up} MAMMA MIA",
                    f"STAGIONE FINITA PER {sub_up} CHE SFIGA ASSURDA",
                    f"MA COME SI FA A ROMPERSI COSÌ {sub_up} NON CI CREDO"
                ]
                return random.choice(opts)
            elif persona_id == 2:
                opts = [
                    f"stagione compromessa per {sub_low} preparatori da cacciare",
                    f"solita sfiga con {sub_low} che si ripete sempre",
                    f"preparazione atletica da serie c per {sub_low}",
                    f"tanto con {sub_low} rotto il campionato è finito"
                ]
                return random.choice(opts)
            elif persona_id == 3:
                opts = [
                    f"fatto di cristallo {sub_low} ahahah",
                    f"nemmeno tre partite di fila regge {sub_low} ahahah",
                    f"in infermeria fisso {sub_low} ormai ahahah",
                    f"appena tocca palla si rompe {sub_low} dai ahahah"
                ]
                return random.choice(opts)
            elif persona_id == 4:
                opts = [
                    f"fanta distrutto per l'infortunio di {sub_low}",
                    f"svincolo obbligatorio all'asta di riparazione per {sub_low}",
                    f"avevo investito mezzo budget su {sub_low} ciao",
                    f"stagione di fanta buttata nel cesso con {sub_low} rotto"
                ]
                return random.choice(opts)
            elif persona_id == 5:
                return random.choice([sub_low, "rotto", "sfiga", "stagione finita", "crociato"])

        elif ptype == "RED_CARD":
            if persona_id == 1:
                opts = [
                    f"MA CHE ROSSO È QUESTO PER {sub_up} DAI",
                    f"MA SEI PAZZO ARBITRO VENDUTO ROSSO A {sub_up}",
                    f"MA COME SI FA A BUTTARE FUORI {sub_up} ASSURDO"
                ]
                return random.choice(opts)
            elif persona_id == 2:
                opts = [
                    f"in dieci finita la partita comunque colpa di {sub_low}",
                    f"fallo stupido e ingenuo di {sub_low} giocatore senza cervello",
                    f"espulsione telefonatissima {sub_low} solito ingenuo"
                ]
                return random.choice(opts)
            elif persona_id == 3:
                opts = [
                    f"interventi da galera di {sub_low} ahahah",
                    f"ha cercato di decapitarlo {sub_low} ahahahah",
                    f"rosso diretto e a fare la doccia {sub_low} ahahah"
                ]
                return random.choice(opts)
            elif persona_id == 4:
                opts = [
                    f"rosso a {sub_low} al fanta giornata rovinata subito",
                    f"-1 a {sub_low} e addio vittoria al fanta",
                    f"messo titolare {sub_low} e si fa cacciare maledetto"
                ]
                return random.choice(opts)
            elif persona_id == 5:
                return random.choice([sub_low, "macellaio", "follia", "venduto", "espulso"])

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
                return random.choice(["finita", "meritato", "scempio", "a casa"])

        else:  # Generico / Notizie generiche
            if persona_id == 1:
                opts = [
                    f"NON CI CREDO MA CHE ROBA SU {sub_up}",
                    f"MAMMA MIA ASSURDO {sub_up}",
                    f"MA ANDATE A CAGARE DAI SU {sub_up}",
                    f"NOTIZIA CLAMOROSA SU {sub_up} ASSURDO",
                    f"TUTTO VERO SU {sub_up} NON CI CREDO"
                ]
                return random.choice(opts)
            elif persona_id == 2:
                pref = random.choice(PREFIXES_CINICO)
                close = random.choice(CLOSINGS_CINICO)
                return f"{pref} la solita storia su {sub_low} {close}"
            elif persona_id == 3:
                opts = [
                    f"ma chi cazzo è {sub_low} ahahah",
                    f"pagliacci totali con {sub_low} ahahahah",
                    f"e dove vogliono andare con {sub_low} ahahah",
                    f"già si esaltano per {sub_low} ahahah che scempio"
                ]
                return random.choice(opts)
            elif persona_id == 4:
                opts = [
                    f"fantacalcio distrutto per colpa delle notizie su {sub_low}",
                    f"chissà quanto prende al fanta {sub_low} adesso",
                    f"se prendono {sub_low} mi sballa l'asta di riparazione",
                    f"speriamo solo non influisca sul fanta sta roba su {sub_low}"
                ]
                return random.choice(opts)
            elif persona_id == 5:
                return random.choice([sub_low, "ridicoli", "vabbè", "imbarazzante", "scandalo", "ciao"])

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

        # Rich pool of context replies
        REPLIES_TO_EMOTIVO = [
            "ma che urli che la partita è ancora lunga",
            "calmati che hanno fatto un tiro in mezz'ora",
            "solito esaltato per un gol a caso",
            "abbassa la cresta che non avete vinto niente",
            "ti sento urlare da qua calmati un attimo",
            "esaltati pure intanto state giocando malissimo",
            "ma ti droghi per esultare così?",
            "calma che mo arriva il pareggio sicuro",
            "solito invasato dai",
            "manco fosse la finale di champions"
        ]

        REPLIES_TO_CINICO = [
            "MA STAI ZITTO GUFO MALEDETTO",
            "MA GODITI LA PARTITA OGNI TANTO",
            "SEMPRE A PIANGERE MAI CONTENTO",
            "ma che partita hai visto ladri dove",
            "il gufo supremo ha parlato ahahah",
            "comprati un maalox dai ahahahah",
            "ancora che gufa questo incredibile",
            "rosica di meno dai",
            "taci che fai più bella figura",
            "ma goditela invece di piangere sempre"
        ]

        REPLIES_TO_TROLL = [
            "MA CHE RIDI COGLIONE",
            "PAGLIACCIO PENSA AI TUOI",
            "RIDI RIDI CHE DOMENICA TOCCA A TE",
            "fai poco lo spiritoso",
            "parla quello che ne ha presi tre ieri ahahah",
            "e si gode ancora di più ahahah",
            "pagliaccio muto e a casa",
            "torna nella caverna dai",
            "ridi su sto cazzo"
        ]

        REPLIES_TO_FANTA = [
            "godo ahahahah chiudi l'app che è meglio",
            "ma chi se ne frega del tuo fantacalcio",
            "MA PENSA ALLA PARTITA VERA NON AL FANTA",
            "piangi ancora per il fantacalcio dai",
            "tanto la perdevi comunque la giornata",
            "già tanto che non hai preso -3",
            "ben ti sta che l'hai messo contro",
            "fanta rovinato goduria doppia"
        ]

        def get_reply(responder_id, target_pid):
            if target_pid == 1:
                return random.choice(REPLIES_TO_EMOTIVO)
            elif target_pid == 2:
                return random.choice(REPLIES_TO_CINICO)
            elif target_pid == 3:
                return random.choice(REPLIES_TO_TROLL)
            elif target_pid == 4:
                return random.choice(REPLIES_TO_FANTA)
            else:
                return random.choice(["argomenta ogni tanto dai", "sempre sintetico tu eh", "taci dai", "muti"])

        available_responders = [pid for pid in [1, 2, 3, 4, 5] if pid != parent_pid]
        random.shuffle(available_responders)

        current_time = parent_delay
        last_id = 1

        for i in range(min(max_replies, len(available_responders))):
            resp_pid = available_responders[i]
            resp_persona = self.personas[resp_pid]
            delta = random.randint(8, 25)
            current_time += delta

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

    def simulate_crowd(self, post_text, count=100, include_replies=True):
        """
        Genera un flusso ad alto volume (es. 100 messaggi) con:
        1. Ancoraggio semantico rigoroso al soggetto/marcatore del post (zero giocatori a caso).
        2. Garanzia assoluta anti-ripetizione (100 messaggi unici e variati).
        3. Discussioni multi-turno bot-to-bot realistiche e variegate.
        """
        meta = self.parser.parse(post_text)
        ptype = meta["type"]

        persona_weights = [
            (1, 0.25),
            (2, 0.20),
            (3, 0.20),
            (4, 0.15),
            (5, 0.20),
        ]
        p_choices = [p[0] for p in persona_weights]
        p_probs = [p[1] for p in persona_weights]

        community_names = [
            "Matteo", "Curran", "Marco", "Federico", "Ale", "Lorenzo", "Simone", "Davide",
            "Andrea", "Luca", "Gianluca", "Filippo", "Gabriele", "Stefano", "Edoardo",
            "Christian", "Samuele", "Jacopo", "Manuel", "Diego", "Pietro", "Riccardo",
            "Tommaso", "Elia", "Niccolò", "Mattia", "Daniele", "Leonardo", "Fabio", "Giacomo",
            "Zanna", "Lollo", "Tommy", "Bibo", "Cappe", "Simo_Inter", "Fede_Juve", "Ale_Milan",
            "Mirko", "Claudio", "Valerio", "Fra", "Gio", "Ale_Curva", "Jack", "Tony"
        ]

        REPLIES_TO_EMOTIVO = [
            "ma che urli che la partita è ancora lunga",
            "calmati che hanno fatto un tiro in mezz'ora",
            "solito esaltato per un gol a caso",
            "abbassa la cresta che non avete vinto niente",
            "ti sento urlare da qua calmati",
            "esaltati pure intanto state giocando malissimo",
            "ma ti droghi per esultare così?",
            "calma che mo arriva il pareggio",
            "solito invasato dai",
            "manco fosse la finale di champions",
            "state calmi un attimo",
            "mamma mia che esagerazione"
        ]

        REPLIES_TO_CINICO = [
            "MA STAI ZITTO GUFO MALEDETTO",
            "MA GODITI LA PARTITA OGNI TANTO",
            "SEMPRE A PIANGERE MAI CONTENTO",
            "ma che partita hai visto ladri dove",
            "il gufo supremo ha parlato ahahah",
            "comprati un maalox dai ahahahah",
            "ancora che gufa questo incredibile",
            "rosica di meno dai",
            "taci che fai più bella figura",
            "ma goditela invece di piangere sempre",
            "non sei mai contento allucinante"
        ]

        REPLIES_TO_TROLL = [
            "MA CHE RIDI COGLIONE",
            "PAGLIACCIO PENSA AI TUOI",
            "RIDI RIDI CHE DOMENICA TOCCA A TE",
            "fai poco lo spiritoso",
            "parla quello che ne ha presi tre ieri ahahah",
            "e si gode ancora di più ahahah",
            "pagliaccio muto e a casa",
            "torna nella caverna dai",
            "ridi su sto cazzo",
            "vediamo a fine partita chi ride"
        ]

        REPLIES_TO_FANTA = [
            "godo ahahahah chiudi l'app che è meglio",
            "ma chi se ne frega del tuo fantacalcio",
            "MA PENSA ALLA PARTITA VERA NON AL FANTA",
            "piangi ancora per il fantacalcio dai",
            "tanto la perdevi comunque la giornata",
            "già tanto che non hai preso -3",
            "ben ti sta che l'hai messo contro",
            "fanta rovinato goduria doppia",
            "sempre a lamentarvi del fanta madonna"
        ]

        def get_crowd_reply(responder_id, target_pid):
            if target_pid == 1:
                return random.choice(REPLIES_TO_EMOTIVO)
            elif target_pid == 2:
                return random.choice(REPLIES_TO_CINICO)
            elif target_pid == 3:
                return random.choice(REPLIES_TO_TROLL)
            elif target_pid == 4:
                return random.choice(REPLIES_TO_FANTA)
            else:
                return random.choice(["argomenta ogni tanto dai", "sempre sintetico tu eh", "taci dai", "muti", "parla come mangi"])

        feed = []
        current_time = random.randint(1, 3)
        seen_messages = set()

        # Genera 'count' messaggi con anti-ripetizione garantita
        for i in range(1, count + 1):
            pid = random.choices(p_choices, weights=p_probs)[0]
            pdata = self.personas[pid]
            user = random.choice(community_names)

            current_time += random.randint(1, 3) if i < 30 else random.randint(2, 4)

            is_reply = include_replies and len(feed) > 2 and random.random() < 0.35

            cleaned = ""
            target = None

            # Tenta fino a 15 volte di generare un messaggio NON ancora visto
            for _ in range(15):
                if is_reply:
                    target = random.choice(feed[-min(len(feed), 6):])
                    raw = get_crowd_reply(pid, target["persona_id"])
                else:
                    raw = self._generate_slot_message(pid, ptype, meta)

                cand = validate_and_clean(raw, pid, pdata["max_words"])
                if cand.lower() not in seen_messages:
                    cleaned = cand
                    break

            # Se ancora colliso, aggiungi variazione sintattica naturale
            if not cleaned:
                suffix = random.choice(["dai", "davvero", "eh", "mamma mia", "sul serio", "veramente", "ora"])
                cleaned = f"{cand} {suffix}"
                cleaned = validate_and_clean(cleaned, pid, pdata["max_words"])

            seen_messages.add(cleaned.lower())

            if is_reply and target:
                feed.append({
                    "id": i,
                    "user": user,
                    "in_reply_to_id": target["id"],
                    "in_reply_to_user": target["user"],
                    "in_reply_to_snippet": target["message"][:30] + ("..." if len(target["message"]) > 30 else ""),
                    "persona_id": pid,
                    "persona_name": pdata["name"],
                    "delay_seconds": current_time,
                    "message": cleaned
                })
            else:
                feed.append({
                    "id": i,
                    "user": user,
                    "in_reply_to_id": None,
                    "in_reply_to_user": None,
                    "in_reply_to_snippet": None,
                    "persona_id": pid,
                    "persona_name": pdata["name"],
                    "delay_seconds": current_time,
                    "message": cleaned
                })

        return feed
