from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .engine import CurransIdeaEngine
from .personas import PERSONAS
from .channel_parser import ChannelPostParser
from .dashboard_html import DASHBOARD_HTML

app = FastAPI(
    title="Humans as Curran's Idea API",
    description=(
        "API REST per la simulazione comportamentale e l'estrazione semantica di commenti Telegram "
        "calibrata su oltre 45.000 messaggi reali con 5 archetipi psicologici."
    ),
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Abilita CORS per permettere a siti web (incluso GitHub Pages) di interrogare l'API senza blocchi
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = CurransIdeaEngine()
parser = ChannelPostParser()


# ----------------- SCHEMI PYDANTIC -----------------

class ParseRequest(BaseModel):
    text: str = Field(..., examples=["GOAL! ⚽️ Lautaro Martinez 👟 Barella ⏱️ 34' Inter 🆚 Milan #SerieA"])

class ParseResponse(BaseModel):
    type: str
    team_home: Optional[str] = None
    team_away: Optional[str] = None
    score: Optional[str] = None
    scorer: Optional[str] = None
    assister: Optional[str] = None
    minute: Optional[str] = None
    player: Optional[str] = None
    competition: Optional[str] = None
    raw_text: str

class SimulateRequest(BaseModel):
    text: str = Field(..., examples=["GOAL! ⚽️ Lautaro Martinez ⏱️ 34' Inter 🆚 Milan"])
    persona_ids: Optional[List[int]] = Field(default=None, description="Filtra personas (1-5), default tutte")

class ReactionItem(BaseModel):
    persona_id: int
    persona_name: str
    delay_seconds: int
    message: str

class SimulateResponse(BaseModel):
    event_type: str
    parsed_metadata: dict
    reactions: List[ReactionItem]

class ThreadRequest(BaseModel):
    text: str = Field(..., examples=["GOAL! ⚽️ Lautaro Martinez ⏱️ 34' Inter 🆚 Milan"])
    max_replies: Optional[int] = Field(default=3, ge=1, le=4, description="Numero di risposte nel thread (1-4)")

class ThreadMessageItem(BaseModel):
    id: int
    in_reply_to_id: Optional[int]
    in_reply_to_persona: Optional[str] = None
    persona_id: int
    persona_name: str
    delay_seconds: int
    message: str

class ThreadResponse(BaseModel):
    event_type: str
    thread: List[ThreadMessageItem]

class CrowdRequest(BaseModel):
    text: str = Field(..., examples=["GOAL! ⚽️ Lautaro Martinez ⏱️ 34' Inter 🆚 Milan"])
    count: Optional[int] = Field(default=100, ge=1, le=200, description="Numero di messaggi da generare (1-200)")
    include_replies: Optional[bool] = Field(default=True, description="Se includere risposte e citazioni bot-to-bot")

class CrowdMessageItem(BaseModel):
    id: int
    user: str
    in_reply_to_id: Optional[int] = None
    in_reply_to_user: Optional[str] = None
    in_reply_to_snippet: Optional[str] = None
    persona_id: int
    persona_name: str
    delay_seconds: int
    message: str

class CrowdResponse(BaseModel):
    event_type: str
    total: int
    feed: List[CrowdMessageItem]


# ----------------- ENDPOINTS -----------------

@app.get("/", tags=["Dashboard & Info"])
def root(request: Request):
    """
    Se visitato da un browser (invia text/html), restituisce la Web Dashboard interattiva in tempo reale.
    Se richiesto da client API o test (invia application/json o */*), restituisce il riepilogo JSON.
    """
    accept = request.headers.get("accept", "")
    if "text/html" in accept:
        return HTMLResponse(content=DASHBOARD_HTML)
    return JSONResponse(content={
        "status": "online",
        "service": "Humans as Curran's Idea API",
        "version": "2.0.0",
        "dashboard_url": "/dashboard",
        "docs_url": "/docs",
        "endpoints": {
            "GET /dashboard": "Web Dashboard interattiva in tempo reale",
            "GET /api/v1/personas": "Lista dei 5 archetipi comportamentali",
            "POST /api/v1/parse": "Estrazione semantica di eventi da post sportivi",
            "POST /api/v1/simulate": "Simulazione commenti con delay realistici",
            "POST /api/v1/thread": "Simulazione di discussione multi-turno bot-to-bot",
            "POST /api/v1/crowd": "Simulazione di folla fino a 100+ commenti in tempo reale"
        }
    })

@app.get("/dashboard", response_class=HTMLResponse, tags=["Dashboard & Info"])
def dashboard():
    """Restituisce la Web Dashboard live in stile Telegram per simulare fino a 100 messaggi in tempo reale."""
    return HTMLResponse(content=DASHBOARD_HTML)

@app.get("/api/v1/info", tags=["Info"])
def api_info():
    """Riepilogo tecnico e stato dell'API in formato JSON."""
    return {
        "status": "online",
        "service": "Humans as Curran's Idea API",
        "version": "2.0.0",
        "docs_url": "/docs"
    }

@app.get("/api/v1/personas", tags=["Personas"])
def get_personas():
    """Restituisce le specifiche e le metriche comportamentali dei 5 archetipi psicologici."""
    return {"total": len(PERSONAS), "personas": list(PERSONAS.values())}

@app.post("/api/v1/parse", response_model=ParseResponse, tags=["Parser"])
def parse_post(req: ParseRequest):
    """Estrae marcatori, assist, squadre, minuto, punteggio e competizione dal post del canale."""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Il testo del post non può essere vuoto.")
    parsed = parser.parse(req.text)
    return parsed

@app.post("/api/v1/simulate", response_model=SimulateResponse, tags=["Simulator"])
def simulate_reactions(req: SimulateRequest):
    """Simula le reazioni immediate dei 5 archetipi sotto al post, ordinate per tempo di reazione umano."""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Il testo del post non può essere vuoto.")
    
    meta = parser.parse(req.text)
    reactions = engine.simulate_mock_reactions(req.text)

    if req.persona_ids:
        reactions = [r for r in reactions if r["persona_id"] in req.persona_ids]

    return {
        "event_type": meta["type"],
        "parsed_metadata": meta,
        "reactions": reactions
    }

@app.post("/api/v1/thread", response_model=ThreadResponse, tags=["Simulator"])
def simulate_thread(req: ThreadRequest):
    """Simula un thread di discussione in cui i diversi archetipi si rispondono e si provocano a vicenda."""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Il testo del post non può essere vuoto.")

    meta = parser.parse(req.text)
    max_replies = req.max_replies or 3
    thread = engine.simulate_thread(req.text, max_replies=max_replies)

    return {
        "event_type": meta["type"],
        "thread": thread
    }

@app.post("/api/v1/crowd", response_model=CrowdResponse, tags=["Simulator"])
def simulate_crowd(req: CrowdRequest):
    """Simula una folla di utenti Telegram (fino a 100+ messaggi) che reagiscono e discutono in tempo reale sotto all'evento."""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Il testo del post non può essere vuoto.")

    meta = parser.parse(req.text)
    count = req.count or 100
    include_replies = True if req.include_replies is None else req.include_replies

    feed = engine.simulate_crowd(req.text, count=count, include_replies=include_replies)

    return {
        "event_type": meta["type"],
        "total": len(feed),
        "feed": feed
    }
