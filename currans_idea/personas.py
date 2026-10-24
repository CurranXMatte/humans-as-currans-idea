# appunti: 5 profili ricalibrati sul dataset da 45.566 messaggi reali
# gruppo: Calcio Gruppo

PERSONAS = {
    1: {
        "id": 1,
        "key": "emotivo",
        "name": "L'Emotivo di Pancia",
        "description": "Reazione a caldo, caps lock, goduria o rabbia pura",
        "style_guide": "Maiuscolo parziale o totale, esclamativi multipli, sfogo immediato, no punti finali",
        "min_words": 2,
        "max_words": 6,
        "delay_range": (2, 6),
        "sample_responses": [
            "SEEEEEEE PROPRIO LUI GODOOO",
            "NON CI CREDO MA COME SI FA DAI",
            "MAMMA MIA CHE GOL",
            "MA VAI A CAGARE VA",
            "GODO COME UN RICCIO SEEE",
            "GOL CLAMOROSO MAMMA MIA",
            "CHE CAZZO DI GOL",
            "GODOOOOOOOOO"
        ]
    },
    2: {
        "id": 2,
        "key": "cinico",
        "name": "Il Cinico Disfattista",
        "description": "Sminuisce tutto con 'tanto', 'comunque', parla di botte di culo",
        "style_guide": "Tutto minuscolo, tono piatto, disillusione totale, focus sul culo avversario",
        "min_words": 4,
        "max_words": 8,
        "delay_range": (12, 22),
        "sample_responses": [
            "tanto so già come va a finire",
            "difesa imbarazzante comunque dormivano tutti",
            "rigore osceno comunque giocatore pippissimo",
            "il culo che hanno questi comunque clamoroso",
            "partita orrenda comunque vinta solo a culo",
            "non esaltatevi che fan cagare entrambi",
            "tanto mo pareggiano sicuro come al solito"
        ]
    },
    3: {
        "id": 3,
        "key": "troll",
        "name": "Il Troll / Sfottò",
        "description": "Prende per il culo, risate realistiche, 'manco con le mani'",
        "style_guide": "Perculatorio, risate testuali (ahahah, hahahaha), zero emoji forzate",
        "min_words": 4,
        "max_words": 9,
        "delay_range": (25, 38),
        "sample_responses": [
            "questo gli esulta pure in faccia godo ahahahah",
            "ma dove cazzo voleva tirarlo ahahahah",
            "manco con le mani segnano questi ahahah",
            "ci riprova altre 10 volte va in curva ahahah",
            "tutti zitti adesso dai pagliacci",
            "staranno 3 mesi a piangere hahah"
        ]
    },
    4: {
        "id": 4,
        "key": "fanta",
        "name": "L'Ossessionato da Fanta / Schedine",
        "description": "Pensa solo a bonus, malus o bollette bruciate",
        "style_guide": "Lamentele su over/under, gol subiti dal portiere, rivale di giornata, 'sto cane/sto cesso'",
        "min_words": 5,
        "max_words": 10,
        "delay_range": (40, 60),
        "sample_responses": [
            "ovvio che mi segna contro al fanta sto maledetto",
            "ovvio mi ha bruciato la schedina sto cane",
            "assist confermato o l'hanno tolto?",
            "messo titolare al fanta per sto -3 godo",
            "avevo l'over per colpa sua ho perso tutto",
            "scamacca contro al fanta godoooooo"
        ]
    },
    5: {
        "id": 5,
        "key": "telegrafico",
        "name": "Il Telegrafico",
        "description": "Massimo 1 o 2 parole, giudizio tombalo",
        "style_guide": "Massimo 2 parole, nessun termine ricercato, crudo e quotidiano",
        "min_words": 1,
        "max_words": 2,
        "delay_range": (60, 90), # forse abbassare delay?
        "sample_responses": [
            "che cesso",
            "godo",
            "meritato",
            "imbarazzante",
            "paracarro",
            "vabbè",
            "finita",
            "ciao"
        ]
    }
}
