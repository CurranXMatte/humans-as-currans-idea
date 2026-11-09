from currans_idea.channel_parser import ChannelPostParser

def test_parse_goal_post():
    parser = ChannelPostParser()
    post = "GOAL! ⚽️ Lautaro Martinez 👟 Barella ⏱️ 34' Inter 🆚 Milan #SerieA"
    data = parser.parse(post)

    assert data["type"] == "GOAL"
    assert data["scorer"] == "Lautaro Martinez"
    assert data["assister"] == "Barella"
    assert "34" in data["minute"]
    assert data["team_home"] == "Inter"
    assert data["team_away"] == "Milan"
    assert data["competition"] == "SerieA"

def test_parse_casual_goal_post():
    parser = ChannelPostParser()
    post = "goal fabrizio romano"
    data = parser.parse(post)

    assert data["type"] == "GOAL"
    assert data["scorer"] == "Fabrizio Romano"
    assert data["subject"] == "Fabrizio Romano"

def test_parse_injury_post():
    parser = ChannelPostParser()
    post = "🚑 COMUNICATO UFFICIALE: Trauma distorsivo al ginocchio per Bremer"
    data = parser.parse(post)

    assert data["type"] == "INJURY"
    assert data["player"] == "Bremer"

def test_parse_full_time():
    parser = ChannelPostParser()
    post = "FINE PARTITA! Juventus 🆚 Napoli 2 - 1"
    data = parser.parse(post)

    assert data["type"] == "FULL_TIME"
    assert data["score"] == "2-1"
    assert data["team_home"] == "Juventus"
    assert data["team_away"] == "Napoli"
