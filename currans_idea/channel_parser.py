import re

# parser intelligente per i post del canale telegram
class ChannelPostParser:
    @staticmethod
    def clean_player_name(name):
        if not name:
            return ""
        # rimuove iniziali puntate tipo "Mbappé K." -> "Mbappé"
        cleaned = re.sub(r'\s+[A-Z]\.?$', '', name.strip())
        return cleaned

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
            
        # 2. Squadre (Flag Team 🆚 Team Flag)
        if "🆚" in post_text:
            parts = post_text.split("🆚")
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
            
        # 3. Classificazione tipo di post
        if "GOAL!" in upper or "GOL!" in upper:
            data["type"] = "GOAL"
            score_m = re.search(r'(\d+)\s*-\s*(\d+)', post_text)
            if score_m:
                data["score"] = f"{score_m.group(1)}-{score_m.group(2)}"
            scorer_m = re.search(r'⚽️\s*([A-Za-zÀ-ÿ\s\.\'\-]+?)(?:\s*👟|\s*⏱️|\n|$)', post_text)
            if scorer_m:
                data["scorer"] = cls.clean_player_name(scorer_m.group(1))
            assist_m = re.search(r'👟\s*([A-Za-zÀ-ÿ\s\.\'\-]+?)(?:\s*⏱️|\n|$)', post_text)
            if assist_m and assist_m.group(1).strip() not in ["---", "-", ""]:
                data["assister"] = cls.clean_player_name(assist_m.group(1))
            min_m = re.search(r'⏱️?\s*(\d+[\'’]?)', post_text)
            if min_m:
                data["minute"] = min_m.group(1).strip()
                
        elif "FORMAZIONI UFFICIALI" in upper:
            data["type"] = "LINEUP"
        elif "FINE PARTITA" in upper or "FINALE!" in upper:
            data["type"] = "FULL_TIME"
            score_m = re.search(r'(\d+)\s*-\s*(\d+)', post_text)
            if score_m:
                data["score"] = f"{score_m.group(1)}-{score_m.group(2)}"
        elif "INTERVALLO" in upper:
            data["type"] = "HALF_TIME"
        elif "INIZIO PARTITA" in upper or "INIZIO SECONDO TEMPO" in upper:
            data["type"] = "MATCH_START"
        elif "CARTELLINO ROSSO" in upper or "ESPULSIONE" in upper:
            data["type"] = "RED_CARD"
        elif "RIGORE" in upper:
            data["type"] = "PENALTY"
        elif "ANNULLATO" in upper:
            data["type"] = "DISALLOWED"
        elif "COMUNICATO UFFICIALE" in upper or "🚑" in post_text or any(k in post_text.lower() for k in ["trauma", "lesione", "crociato", "distorsivo"]):
            data["type"] = "INJURY"
            doc_m = re.search(r'(?:comunicato che|ufficiale\s*:?|nei confronti di|infortunio a|infortunio per|lesione per|per|di)\s+([A-ZÀ-ÿ][a-zà-ÿ]+(?:\s+[A-ZÀ-ÿ][a-zà-ÿ]+)?)', post_text)
            if doc_m:
                data["player"] = doc_m.group(1).strip()
                
        return data
