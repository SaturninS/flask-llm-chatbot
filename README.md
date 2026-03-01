# flask-llm-chatbot

Chatbot Flask avec streaming SSE et API Mistral. Gestion du contexte conversationnel et system prompt paramétrable.

## Architecture

```
POST /chat  ──►  Flask  ──►  Mistral API  ──►  SSE stream
GET  /health ──► {"status": "ok"}
```

## Installation locale

```bash
# 1. Créer et activer un environnement virtuel
python3 -m venv .venv
source .venv/bin/activate       # Linux / macOS
# .venv\Scripts\activate        # Windows

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer la clé API
cp .env.example .env
# Renseigner MISTRAL_API_KEY dans .env

# 4. Lancer l'application
python app.py
```

## Docker

```bash
docker compose up --build
```

## Exemples curl

### Health check

```bash
curl http://localhost:5000/health
```

### Chat simple

```bash
curl -N -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Quels sont les symptômes de la grippe ?"}'
```

### Chat avec historique

```bash
curl -N -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Et le traitement ?",
    "messages": [
      {"role": "user", "content": "Quels sont les symptômes de la grippe ?"},
      {"role": "assistant", "content": "Fièvre, courbatures, fatigue, toux sèche."}
    ]
  }'
```

### System prompt personnalisé

```bash
curl -N -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Bonjour",
    "system_prompt": "Tu es un assistant juridique spécialisé en droit français."
  }'
```

## CI

GitHub Actions : lint `ruff` + test `/health` à chaque push.
