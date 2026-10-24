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
        teams_m = re.search(r'[^\w\n]*([A-Za-z0-9\s]+?)\s*🆚\s*([A-Za-z0-9\s]+?)(?:[\n⚫️🔵🔴⚪️🟡🟣]|$)', post_text)
        if teams_m:
            data["team_home"] = teams_m.group(1).strip()
            data["team_away"] = teams_m.group(2).strip()
            
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
            # cerca nome giocatore se presente
            doc_m = re.search(r'(?:comunicato che|ufficiale\s*:?|nei confronti di)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', post_text)
            if doc_m:
                data["player"] = doc_m.group(1)
                
        return data
