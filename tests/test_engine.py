from currans_idea.engine import CurransIdeaEngine
from currans_idea.personas import PERSONAS

def test_engine_simulate_reactions():
    engine = CurransIdeaEngine()
    post = "GOAL! ⚽️ Vlahovic ⏱️ 12' Juventus 🆚 Lazio"
    reactions = engine.simulate_mock_reactions(post)

    assert len(reactions) == 5
    persona_ids = {r["persona_id"] for r in reactions}
    assert persona_ids == {1, 2, 3, 4, 5}

    # Verifica ordinamento delay
    delays = [r["delay_seconds"] for r in reactions]
    assert delays == sorted(delays)

    # Verifica nessuna punteggiatura finale da boomer (punto fermo)
    for r in reactions:
        assert not r["message"].endswith(".")

def test_engine_simulate_thread():
    engine = CurransIdeaEngine()
    post = "GOAL! ⚽️ Leao ⏱️ 88' Milan 🆚 Roma"
    thread = engine.simulate_thread(post, max_replies=3)

    assert len(thread) >= 2
    assert thread[0]["id"] == 1
    assert thread[0]["in_reply_to_id"] is None

    # I messaggi successivi devono avere in_reply_to_id valido
    valid_ids = {1}
    for item in thread[1:]:
        assert item["in_reply_to_id"] in valid_ids
        valid_ids.add(item["id"])
