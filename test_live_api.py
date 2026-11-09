import sys
import json
import urllib.request
import urllib.error

def test_api(base_url):
    base_url = base_url.rstrip("/")
    print("=" * 65)
    print(f"🚀 TEST SERVER API LIVE: {base_url}")
    print("=" * 65)

    # 1. Health check
    print("\n1️⃣  Test Root Endpoint (GET /)...")
    try:
        with urllib.request.urlopen(f"{base_url}/", timeout=10) as resp:
            data = json.loads(resp.read().decode())
            print(f"   ✅ Status HTTP: {resp.status}")
            print(f"   Risposta: {data['service']} v{data['version']} (Status: {data['status']})")
    except Exception as e:
        print(f"   ❌ Errore connessione: {e}")
        return

    # 2. Test Personas
    print("\n2️⃣  Test Archetipi (GET /api/v1/personas)...")
    try:
        with urllib.request.urlopen(f"{base_url}/api/v1/personas", timeout=10) as resp:
            data = json.loads(resp.read().decode())
            print(f"   ✅ Archetipi caricati: {data['total']}")
            for p in data["personas"]:
                print(f"      - [{p['id']}] {p['name']} ({p['delay_range'][0]}-{p['delay_range'][1]}s)")
    except Exception as e:
        print(f"   ❌ Errore: {e}")

    # 3. Test Simulate Gol Post
    print("\n3️⃣  Test Simulazione Commenti (POST /api/v1/simulate)...")
    payload = {
        "text": "GOAL! ⚽️ Lautaro Martinez 👟 Barella ⏱️ 34' Inter 🆚 Milan #SerieA"
    }
    req = urllib.request.Request(
        f"{base_url}/api/v1/simulate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            res = json.loads(resp.read().decode())
            print(f"   ✅ Evento rilevato: {res['event_type']}")
            print(f"   Marcatore: {res['parsed_metadata'].get('scorer')} | Assist: {res['parsed_metadata'].get('assister')}")
            print(f"   Reazioni generate:")
            for r in res["reactions"]:
                print(f"      [+{r['delay_seconds']}s] ({r['persona_name']}): {r['message']}")
    except Exception as e:
        print(f"   ❌ Errore: {e}")

    # 4. Test Thread Multi-Turno
    print("\n4️⃣  Test Discussione a Catena Bot-to-Bot (POST /api/v1/thread)...")
    thread_payload = {
        "text": "GOAL! ⚽️ Vlahovic ⏱️ 89' Juventus 🆚 Napoli",
        "max_replies": 3
    }
    thread_req = urllib.request.Request(
        f"{base_url}/api/v1/thread",
        data=json.dumps(thread_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(thread_req, timeout=15) as resp:
            t_res = json.loads(resp.read().decode())
            print(f"   ✅ Thread generato ({len(t_res['thread'])} messaggi):")
            for msg in t_res["thread"]:
                reply_to = f" (in risposta a #{msg['in_reply_to_id']} {msg['in_reply_to_persona']})" if msg["in_reply_to_id"] else " (Post Canale)"
                print(f"      [#{msg['id']} | +{msg['delay_seconds']}s]{reply_to} {msg['persona_name']}:")
                print(f"         > {msg['message']}")
    except Exception as e:
        print(f"   ❌ Errore: {e}")

    # 5. Test Crowd Feed (100 messaggi in tempo reale)
    print("\n5️⃣  Test Folla Telegram (100 messaggi) (POST /api/v1/crowd)...")
    crowd_payload = {
        "text": "GOAL! ⚽️ Lautaro Martinez ⏱️ 34' Inter 🆚 Milan #SerieA",
        "count": 100,
        "include_replies": True
    }
    crowd_req = urllib.request.Request(
        f"{base_url}/api/v1/crowd",
        data=json.dumps(crowd_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(crowd_req, timeout=20) as resp:
            c_res = json.loads(resp.read().decode())
            print(f"   ✅ Folla generata con successo: {c_res['total']} messaggi!")
            print(f"      Primo messaggio: [{c_res['feed'][0]['user']}]: {c_res['feed'][0]['message']}")
            print(f"      Ultimo messaggio (#{c_res['total']}): [{c_res['feed'][-1]['user']} | +{c_res['feed'][-1]['delay_seconds']}s]: {c_res['feed'][-1]['message']}")
    except Exception as e:
        print(f"   ❌ Errore: {e}")

    print("\n" + "=" * 65)
    print(f"✨ Test completato con successo! Swagger docs: {base_url}/docs")
    print("=" * 65)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    test_api(target)
