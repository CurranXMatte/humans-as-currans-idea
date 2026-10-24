import re

# lista parole vietate (troppo da boomer o giornalisti tv)
BANNED_EXPRESSIONS = [
    "i cugini",
    "la compagine",
    "la compagine ospite",
    "la compagine di casa",
    "la dea",
    "il biscione",
    "i nerazzurri",
    "i rossoneri",
    "i bianconeri",
    "il derby della madonnina",
    "estremo difensore",
    "rettangolo verde",
    "massima serie",
    "telefonatissimo",
    "geometrico",
    "magistrale",
    "pregevole",
    "chirurgico",
    "impeccabile",
    "consueto"
]

def clean_trailing_punctuation(text):
    text = text.strip()
    while text.endswith("."):
        text = text[:-1].strip()
    return text

def validate_banned_words(text):
    lower = text.lower()
    for b in BANNED_EXPRESSIONS:
        if b in lower:
            return False
    return True

# todo: rivedere lunghezza max per il cinico
def validate_and_clean(text, persona_id, max_words):
    text = clean_trailing_punctuation(text)
    
    if not validate_banned_words(text):
        # da gestire meglio l'eccezione
        raise ValueError(f"bloccato per parole cringe: {text}")
        
    words = text.split()
    if len(words) > max_words:
        text = " ".join(words[:max_words])
        text = clean_trailing_punctuation(text)
        
    return text
