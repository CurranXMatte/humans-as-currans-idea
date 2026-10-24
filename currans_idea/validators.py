"""
Heuristic validators to prevent artificial/robotic language patterns.
Based on empirical analysis of real Telegram chat logs.
"""
import re

BANNED_EXPRESSIONS = [
    # Boomer / Journalistic TV clichés
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
    
    # Overly academic / artificial words
    "telefonatissimo",
    "geometrico",
    "magistrale",
    "pregevole",
    "chirurgico",
    "impeccabile",
    "consueto"
]

def clean_trailing_punctuation(text: str) -> str:
    """Removes trailing dots or formal terminal marks."""
    text = text.strip()
    while text.endswith("."):
        text = text[:-1].strip()
    return text

def validate_banned_words(text: str) -> bool:
    """Returns False if text contains any banned boomer/journalist expressions."""
    lower = text.lower()
    for banned in BANNED_EXPRESSIONS:
        if banned in lower:
            return False
    return True

def validate_and_clean(text: str, persona_id: int, max_words: int) -> str:
    """
    Cleans text and ensures it adheres to human chat heuristics.
    """
    text = clean_trailing_punctuation(text)
    
    if not validate_banned_words(text):
        raise ValueError(f"Text contains banned journalist/boomer vocabulary: '{text}'")
        
    words = text.split()
    if len(words) > max_words:
        text = " ".join(words[:max_words])
        text = clean_trailing_punctuation(text)
        
    return text
