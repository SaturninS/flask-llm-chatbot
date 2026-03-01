# flask-llm-chatbot

Chatbot Flask avec streaming SSE et API Anthropic Claude. Gestion du contexte conversationnel et system prompt paramétrable.

## Architecture

```
POST /chat  ──►  Flask  ──►  Anthropic API  ──►  SSE stream
GET  /health ──► {"status": "ok"}
```

## Installation

```bash
cp .env.example .env
# Renseigner ANTHROPIC_API_KEY dans .env

pip install -r requirements.txt
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
