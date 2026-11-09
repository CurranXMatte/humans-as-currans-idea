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

HANGING_WORDS = {
    "in", "di", "a", "da", "con", "su", "per", "tra", "fra",
    "il", "lo", "la", "i", "gli", "le", "un", "uno", "una",
    "che", "e", "ma", "o", "del", "dello", "della", "dei", "degli", "delle", "al", "allo", "alla", "ai", "agli", "alle"
}

def validate_and_clean(text, persona_id, max_words):
    text = clean_trailing_punctuation(text)
    
    if not validate_banned_words(text):
        raise ValueError(f"bloccato per parole cringe: {text}")
        
    words = text.split()
    if len(words) > max_words:
        truncated = words[:max_words]
        while truncated and truncated[-1].lower() in HANGING_WORDS:
            truncated.pop()
        text = " ".join(truncated)
        text = clean_trailing_punctuation(text)
        
    return text
