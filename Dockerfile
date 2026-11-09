FROM python:3.12-slim

# Crea utente con UID 1000 (standard di sicurezza per Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY --chown=user requirements.txt pyproject.toml README.md ./
RUN pip install --no-cache-dir --user -r requirements.txt

COPY --chown=user currans_idea/ currans_idea/
COPY --chown=user main.py ./

# Hugging Face Spaces richiede per convenzione la porta 7860
EXPOSE 7860

CMD ["uvicorn", "currans_idea.api:app", "--host", "0.0.0.0", "--port", "7860"]
