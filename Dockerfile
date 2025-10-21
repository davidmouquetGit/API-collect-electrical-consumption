# Image de base
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers requirements
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l’application
COPY app ./app

RUN mkdir -p /var/log/myapp

RUN chmod -R 777 /var/log/myapp

# Exposer le port
EXPOSE 8000

# Commande pour lancer l’API avec Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


