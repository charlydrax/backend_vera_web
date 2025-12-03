# Base légère
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copier requirements pour cache
COPY requirements.txt .

# Installer dépendances système + Python
RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 tesseract-ocr && \
    pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
