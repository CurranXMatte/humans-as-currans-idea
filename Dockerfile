FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt pyproject.toml README.md ./
RUN pip install --no-cache-dir -r requirements.txt

COPY currans_idea/ currans_idea/
COPY main.py ./

EXPOSE 8000

CMD ["uvicorn", "currans_idea.api:app", "--host", "0.0.0.0", "--port", "8000"]
