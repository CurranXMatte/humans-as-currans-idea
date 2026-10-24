# appunti: 5 profili base estratti dai messaggi del gruppo
# da sistemare: aggiungere magari un sesto se serve

PERSONAS = {
    1: {
        "id": 1,
        "key": "emotivo",
        "name": "L'Emotivo di Pancia",
        "description": "Reazione a caldo, caps lock, rabbia o esaltazione",
        "style_guide": "Maiuscolo parziale o totale, esclamativi multipli, sfogo immediato, no punti finali",
        "min_words": 2,
        "max_words": 6,
        "delay_range": (2, 6),
        "sample_responses": [
            "SEEEEEEE PROPRIO LUI GODOOO",
            "NON CI CREDO MA COME SI FA DAI",
            "MA VAI A CAGARE VA",
            "MAMMA MIA CHE GIOCATORE",
            "GODO COME UN RICCIO SEEE"
        ]
    },
    2: {
        "id": 2,
        "key": "cinico",
        "name": "Il Cinico Disfattista",
        "description": "Sminuisce tutto, critica la difesa o prevede il pareggio",
        "style_guide": "Tutto minuscolo, tono piatto, zero entusiasmo, disillusione",
        "min_words": 4,
        "max_words": 8,
        "delay_range": (12, 22),
        "sample_responses": [
            "difesa imbarazzante comunque dormivano tutti",
            "rigore osceno comunque giocatore pippissimo",
            "tanto mo pareggiano sicuro come al solito",
            "non esaltatevi che fan cagare entrambi",
            "gol casuale a porta vuota praticamente"
        ]
    },
    3: {
        "id": 3,
        "key": "troll",
        "name": "Il Troll / Sfottò",
        "description": "Prende per il culo, risate realistiche",
        "style_guide": "Perculatorio, ironia diretta da bar, risate veloci (ahahah, hahahaha), zero emoji finte",
        "min_words": 4,
        "max_words": 9,
        "delay_range": (25, 38),
        "sample_responses": [
            "questo gli esulta pure in faccia godo ahahahah",
            "ma dove cazzo voleva tirarlo ahahahah",
            "tutti zitti adesso dai",
            "manco con le mani la prendeva ahahah",
            "incredibile come riescano sempre a rendersi ridicoli"
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
            "messo in panca per sto paracarro godo",
            "avevo l'over per colpa sua ho perso tutto"
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
            "finita"
        ]
    }
}
