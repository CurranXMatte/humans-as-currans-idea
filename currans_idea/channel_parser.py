import re

# Parser intelligente per i post del canale telegram e input in linguaggio naturale
class ChannelPostParser:
    @staticmethod
    def clean_player_name(name):
        if not name:
            return ""
        # Rimuove punteggiatura superflua, 'per', 'di', o iniziali puntate tipo "Mbappé K." -> "Mbappé"
        cleaned = re.sub(r'^(?:di|per|a|su|goal|gol|rete)\s+', '', name.strip(), flags=re.IGNORECASE)
        cleaned = re.sub(r'\s+[A-Z]\.?$', '', cleaned.strip())
        words = cleaned.split()
        return " ".join(w.capitalize() for w in words) if words else ""

    @classmethod
    def parse(cls, post_text):
        data = {
            "type": "NEWS",
            "team_home": None,
            "team_away": None,
            "score": None,
            "scorer": None,
            "assister": None,
            "minute": None,
            "player": None,
            "subject": None,
            "competition": None,
            "raw_text": post_text
        }
        
        upper = post_text.upper()
        
        # 1. Competizione
        comp_m = re.search(r'#(ChampionsLeague|SerieA|EuropaLeague|CoppaItalia|ConferenceLeague|LaLiga|PremierLeague)', post_text, re.IGNORECASE)
        if comp_m:
            data["competition"] = comp_m.group(1)
        elif "CHAMPIONS LEAGUE" in upper:
            data["competition"] = "Champions League"
        elif "SERIE A" in upper:
            data["competition"] = "Serie A"
            
        # 2. Squadre (Flag Team 🆚 Team Flag, o Team vs Team)
        if "🆚" in post_text or re.search(r'\bvs\b', post_text, re.IGNORECASE):
            delimiter = "🆚" if "🆚" in post_text else re.search(r'\bvs\b', post_text, re.IGNORECASE).group(0)
            parts = post_text.split(delimiter)
            before = parts[0].strip().split("\n")[-1]
            after = parts[1].strip().split("\n")[0]

            tokens = re.split(r'[\n⚽️👟⏱️🚑🔴⚫️🔵⚪️🟡🟣!?:;\'"’\-]', before)
            non_empty = [t.strip() for t in tokens if t.strip()]
            home_raw = non_empty[-1] if non_empty else before
            m_home = re.findall(r'[A-Za-zÀ-ÿ0-9]+', home_raw)
            if m_home:
                data["team_home"] = " ".join(m_home)

            after_clean = re.split(r'#|\d+\s*-\s*\d+|[\n⚽️👟⏱️🚑🔴⚫️🔵⚪️🟡🟣!?:;\'"’\-]', after)[0]
            m_away = re.findall(r'[A-Za-zÀ-ÿ0-9]+', after_clean)
            if m_away:
                data["team_away"] = " ".join(m_away)
            
        # 3. Classificazione tipo di post e entità
        is_goal = bool(re.search(r'\b(GOAL|GOL|RETE|SEGNA|HA SEGNATO)\b', upper) or "⚽" in post_text)
        
        if is_goal:
            data["type"] = "GOAL"
            score_m = re.search(r'(\d+)\s*-\s*(\d+)', post_text)
            if score_m:
                data["score"] = f"{score_m.group(1)}-{score_m.group(2)}"
            
            # Cerca marcatore dopo l'emoji ⚽️
            ball_matches = re.findall(r'⚽️?\s*([A-Za-zÀ-ÿ\s\.\'\-]+?)(?:\s*👟|\s*⏱️|\s*#|\s*🆚|\d+\s*-\s*\d+|$|\n)', post_text)
            for cand in ball_matches:
                cand = cand.strip()
                cand = re.sub(r'^(?:GOAL|GOL|RETE)[!\s]*', '', cand, flags=re.IGNORECASE).strip()
                if cand and not re.search(r'^(GOAL|GOL|RETE)$', cand, re.IGNORECASE):
                    data["scorer"] = cls.clean_player_name(cand)
                    break

            # Fallback marcatore linguaggio naturale: "goal fabrizio romano", "gol di leao", "ha segnato osimhen"
            if not data["scorer"]:
                nat_m = re.search(r'(?:goal|gol|rete|segna|ha segnato)\s+(?:di\s+|per\s+)?([A-Za-zÀ-ÿ\s\.\'\-]+?)(?:\s*👟|\s*⏱️|\s*#|\s*🆚|\d+\s*-\s*\d+|$|\n)', post_text, re.IGNORECASE)
                if nat_m:
                    cand = nat_m.group(1).strip()
                    if cand and not re.search(r'^(GOAL|GOL|RETE)$', cand, re.IGNORECASE):
                        data["scorer"] = cls.clean_player_name(cand)

            # Cerca assistman
            assist_m = re.search(r'(?:👟|assist\s+(?:di\s+)?)\s*([A-Za-zÀ-ÿ\s\.\'\-]+?)(?:\s*⏱️|\s*#|\s*🆚|\d+\s*-\s*\d+|$|\n)', post_text, re.IGNORECASE)
            if assist_m and assist_m.group(1).strip() not in ["---", "-", ""]:
                data["assister"] = cls.clean_player_name(assist_m.group(1))

            min_m = re.search(r'⏱️?\s*(\d+[\'’]?)', post_text)
            if min_m:
                data["minute"] = min_m.group(1).strip()
                
        elif "FORMAZIONI UFFICIALI" in upper or "TITOLARI" in upper:
            data["type"] = "LINEUP"
        elif "FINE PARTITA" in upper or "FINALE!" in upper or "FINALE" in upper:
            data["type"] = "FULL_TIME"
            score_m = re.search(r'(\d+)\s*-\s*(\d+)', post_text)
            if score_m:
                data["score"] = f"{score_m.group(1)}-{score_m.group(2)}"
        elif "INTERVALLO" in upper or "FINE PRIMO TEMPO" in upper:
            data["type"] = "HALF_TIME"
        elif "INIZIO PARTITA" in upper or "INIZIO SECONDO TEMPO" in upper:
            data["type"] = "MATCH_START"
        elif re.search(r'\b(CARTELLINO ROSSO|ESPULSIONE|ESPULSO)\b', upper) or "🟥" in post_text:
            data["type"] = "RED_CARD"
            red_m = re.search(r'(?:rosso|espulsione|espulso)\s*(?:a|per|di|diretto)?\s*([A-Za-zÀ-ÿ\s\.\'\-]+?)(?:\s*#|\s*al\s*\d+|\s*⏱️|$|\n)', post_text, re.IGNORECASE)
            if red_m:
                data["player"] = cls.clean_player_name(red_m.group(1))
        elif "RIGORE" in upper:
            data["type"] = "PENALTY"
        elif "ANNULLATO" in upper:
            data["type"] = "DISALLOWED"
        elif "COMUNICATO UFFICIALE" in upper or "🚑" in post_text or any(k in post_text.lower() for k in ["trauma", "lesione", "crociato", "distorsivo", "infortunio"]):
            data["type"] = "INJURY"
            doc_m = re.search(r'(?:per|di|infortunio a|infortunio per|lesione per)\s+([A-ZÀ-ÿ][a-zà-ÿ]+(?:\s+[A-ZÀ-ÿ][a-zà-ÿ]+)?)', post_text)
            if doc_m:
                data["player"] = cls.clean_player_name(doc_m.group(1))
            else:
                nat_doc = re.search(r'(?:infortunio|trauma|lesione|rotto)\s+([A-Za-zÀ-ÿ\s]+?)(?:\s*#|$|\n)', post_text, re.IGNORECASE)
                if nat_doc:
                    data["player"] = cls.clean_player_name(nat_doc.group(1))

        # 4. Imposta subject prioritario: chiunque sia l'entità principale dell'evento
        if data["scorer"]:
            data["subject"] = data["scorer"]
        elif data["player"]:
            data["subject"] = data["player"]
        elif data["team_home"]:
            data["subject"] = data["team_home"]
        else:
            # Fallback per post generici: estrai il primo nome proprio o parola chiave escludendo hashtag/campionati/goal
            clean_tokens = [w for w in re.findall(r'[A-Za-zÀ-ÿ0-9]+', post_text) if len(w) > 2 and w.lower() not in {"goal", "gol", "rete", "seriea", "championsleague", "europaleague", "laliga", "premierleague", "del", "della", "degli", "delle", "con", "per", "tra", "fra", "che", "non", "dal", "dallo", "nel", "nella", "dei", "sul", "sulla", "post", "canale", "ufficiale"}]
            if clean_tokens:
                data["subject"] = " ".join(w.capitalize() for w in clean_tokens[:2])
            else:
                data["subject"] = "la squadra"

        return data
