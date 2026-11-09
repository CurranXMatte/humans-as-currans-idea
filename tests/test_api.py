from fastapi.testclient import TestClient
from currans_idea.api import app

client = TestClient(app)

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "endpoints" in data

def test_api_personas():
    response = client.get("/api/v1/personas")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["personas"]) == 5

def test_api_parse():
    response = client.post("/api/v1/parse", json={"text": "GOAL! ⚽️ Kvaratskhelia ⏱️ 60' Napoli 🆚 Inter"})
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "GOAL"
    assert data["scorer"] == "Kvaratskhelia"

def test_api_simulate():
    response = client.post("/api/v1/simulate", json={"text": "GOAL! ⚽️ Kvaratskhelia ⏱️ 60' Napoli 🆚 Inter"})
    assert response.status_code == 200
    data = response.json()
    assert "reactions" in data
    assert len(data["reactions"]) == 5

def test_api_thread():
    response = client.post("/api/v1/thread", json={"text": "GOAL! ⚽️ Kvaratskhelia ⏱️ 60' Napoli 🆚 Inter", "max_replies": 3})
    assert response.status_code == 200
    data = response.json()
    assert "thread" in data
    assert len(data["thread"]) == 4  # 1 genitore + 3 risposte

def test_api_empty_post_error():
    response = client.post("/api/v1/simulate", json={"text": "   "})
    assert response.status_code == 400
