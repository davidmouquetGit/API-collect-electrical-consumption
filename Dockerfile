# Image Python légère
FROM python:3.11-slim

# Crée un dossier pour l'app
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose le port 8000
EXPOSE 8000

# Charger les variables d'environnement
ENV PYTHONUNBUFFERED=1

# Commande de lancement
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]