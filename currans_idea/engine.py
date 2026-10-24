import random
import re
from .personas import PERSONAS
from .validators import validate_and_clean
from .channel_parser import ChannelPostParser

# matrice combinatoria base
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

    def simulate_mock_reactions(self, post_text):
        # 1. Parsing semantico intelligente del post del canale
        meta = self.parser.parse(post_text)
        ptype = meta["type"]
        scorer = meta["scorer"] or "lui"
        assister = meta["assister"]
        team_home = meta["team_home"] or "squadra"
        team_away = meta["team_away"] or "avversari"
        score = meta["score"]
        minute = meta["minute"]
        player = meta["player"] or scorer

        delays = self.get_delays()
        results = []

        for pid in sorted(self.personas.keys()):
            p = self.personas[pid]
            delay = delays[pid]

            if ptype == "GOAL":
                if pid == 1: # Emotivo
                    opts = [
                        f"SEEEEEEE {scorer.upper()} GODOOO",
                        f"MAMMA MIA CHE GOL DI {scorer.upper()}",
                        f"GODOOOO FINALMENTE {scorer.upper()}",
                        f"GOL ASSURDO DI {scorer.upper()} SEEEE"
                    ]
                    msg = random.choice(opts)
                elif pid == 2: # Cinico
                    opts = [
                        f"difesa del {team_away.lower()} imbarazzante dormivano tutti",
                        f"gol a culo comunque tanto mo pareggiano",
                        f"solita botta di culo di {scorer.lower()}",
                        f"partita orrenda comunque vinta solo a culo"
                    ]
                    msg = random.choice(opts)
                elif pid == 3: # Troll
                    opts = [
                        f"questo gli esulta pure in faccia godo ahahahah",
                        f"tifosi del {team_away.lower()} già a piangere ahahah",
                        f"{scorer.lower()} li zittisce tutti ahahahah",
                        f"nemmeno con le mani la prendevano ahahah"
                    ]
                    msg = random.choice(opts)
                elif pid == 4: # Fanta
                    if assister:
                        opts = [
                            f"assist confermato a {assister.lower()} o lo tolgono?",
                            f"ho {scorer.lower()} al fanta godoooo",
                            f"assist di {assister.lower()} godo per il +1",
                            f"ovvio che mi segna contro {scorer.lower()} sto cane"
                        ]
                    else:
                        opts = [
                            f"ovvio che mi segna contro {scorer.lower()} maledetto",
                            f"ce l'ho contro al fanta porco dio",
                            f"ho {scorer.lower()} al fanta godoooooo",
                            f"mi ha bruciato la schedina sto gol"
                        ]
                    msg = random.choice(opts)
                elif pid == 5: # Telegrafico
                    msg = random.choice([scorer.lower(), "godo", "meritato", "finita"])

            elif ptype == "LINEUP":
                if pid == 1:
                    msg = random.choice(["DAI RAGAZZI CARICHI FORZA", "FORMAZIONE TOP SI VINCE", "MAMMA MIA CHE SQUADRA"])
                elif pid == 2:
                    msg = random.choice(["formazione oscena comunque prevedo disastri", "solite scelte senza senso del mister", "con questi titolari non si va da nessuna parte"])
                elif pid == 3:
                    msg = random.choice(["ancora titolare sto cesso ahahah", "questi stasera ne prendono quattro ahahah", "in panchina a piangere ahahah"])
                elif pid == 4:
                    msg = random.choice(["chi avete titolare al fanta?", "messo in panchina sto cane maledetto", "ballottaggio perso al fanta ovvio"])
                elif pid == 5:
                    msg = random.choice(["disastro", "vittoria facile", "vabbè"])

            elif ptype == "INJURY":
                if pid == 1:
                    msg = random.choice(["NOOO CHE BRUTTO INFORTUNIO SPERIAMO BENE", "SPERIAMO NIENTE DI GRAVE MAMMA MIA", "STAGIONE FINITA CHE SFIGA"])
                elif pid == 2:
                    msg = random.choice(["stagione compromessa comunque preparatori atletici da cacciare", "solita sfiga che si ripete sempre", "preparazione atletica da serie c"])
                elif pid == 3:
                    msg = random.choice(["fatto di cristallo questo giocatore ahahah", "nemmeno tre partite di fila regge", "in infermeria fisso ormai"])
                elif pid == 4:
                    msg = random.choice(["fanta distrutto per colpa dell'infortunio ciao", "svincolo obbligatorio all'asta di riparazione", "avevo investito mezzo budget su di lui"])
                elif pid == 5:
                    msg = random.choice(["rotto", "sfiga", "finita"])

            elif ptype == "FULL_TIME":
                if pid == 1:
                    msg = random.choice(["FINITAAAAA GODOOO CHE PARTITA", "SEEE VITTORIA MERITATA RAGAZZI", "CHE SCHIFO DI PARTITA NON CI CREDO"])
                elif pid == 2:
                    msg = random.choice(["partita orrenda comunque vinta solo a culo", "tanto non andranno mai da nessuna parte", "zero gioco solita prestazione ridicola"])
                elif pid == 3:
                    msg = random.choice(["tutti a casa e a nanna adesso dai ahahah", "tifosi muti stasera ahahahah", "pagliacci totali a casa"])
                elif pid == 4:
                    msg = random.choice(["giornata di fanta chiusa con una sconfitta", "schedina saltata per questa partita", "al fanta ho perso di mezzo punto"])
                elif pid == 5:
                    msg = random.choice(["finita", "meritato", "scempio"])

            elif ptype == "HALF_TIME":
                if pid == 1:
                    msg = random.choice(["SVEGLIATEVI NEL SECONDO TEMPO DAI", "MAMMA MIA CHE PRIMO TEMPO"])
                elif pid == 2:
                    msg = random.choice(["primo tempo orrendo comunque zero tiri", "partita da addormentarsi proprio"])
                elif pid == 3:
                    msg = random.choice(["che partitaccia oscena ahahah", "manco nei dilettanti ahahah"])
                elif pid == 4:
                    msg = random.choice(["zero bonus in questo primo tempo", "speriamo nei cambi per il fanta"])
                elif pid == 5:
                    msg = random.choice(["dormono", "orrendo", "vabbè"])

            elif ptype == "RED_CARD":
                if pid == 1:
                    msg = random.choice(["MA CHE ROSSO È QUESTO DAI", "MA SEI PAZZO ARBITRO VENDUTO"])
                elif pid == 2:
                    msg = random.choice(["in dieci finita la partita comunque", "fallo stupido e ingenuo giocatore senza cervello"])
                elif pid == 3:
                    msg = random.choice(["interventi da galera ahahah", "ha cercato di decapitarlo ahahahah"])
                elif pid == 4:
                    msg = random.choice(["rosso al fanta giornata rovinata subito", "-1 e addio vittoria al fanta"])
                elif pid == 5:
                    msg = random.choice(["macellaio", "follia", "venduto"])

            elif ptype == "DISALLOWED":
                if pid == 1:
                    msg = random.choice(["LADRI CLAMOROSI NON CI CREDO", "GODO ANNULLATO SEEE"])
                elif pid == 2:
                    msg = random.choice(["fuorigioco di un millimetro solita farsa", "tanto con questo var non si capisce niente"])
                elif pid == 3:
                    msg = random.choice(["il var colpisce ancora ahahahah goduria", "già avevano esultato ahahah che pagliacci"])
                elif pid == 4:
                    msg = random.choice(["mi hanno tolto il bonus al fanta ladri", "schedina saltata per un millimetro"])
                elif pid == 5:
                    msg = random.choice(["farsa", "annullato", "ladri"])

            else: # Generico / News
                if pid == 1:
                    msg = random.choice(["NON CI CREDO MA CHE ROBA È", "MAMMA MIA ASSURDO", "MA ANDATE A CAGARE DAI"])
                elif pid == 2:
                    msg = random.choice(["comunque una pagliacciata ridicola", "tanto so già come va a finire", "solita farsa senza vergogna"])
                elif pid == 3:
                    msg = random.choice(["ma chi cazzo sono questi ahahah", "pagliacci totali ahahahah", "e dove vogliono andare ahahah"])
                elif pid == 4:
                    msg = random.choice(["fantacalcio distrutto per colpa di ste notizie", "chissà quanto prende al fanta questo"])
                elif pid == 5:
                    msg = random.choice(["ridicoli", "vabbè", "imbarazzante"])

            cleaned = validate_and_clean(msg, pid, p["max_words"])
            results.append({
                "persona_id": pid,
                "persona_name": p["name"],
                "delay_seconds": delay,
                "message": cleaned
            })

        results.sort(key=lambda x: x["delay_seconds"])
        return results
