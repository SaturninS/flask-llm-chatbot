import os
import json
from flask import Flask, request, jsonify, Response, stream_with_context
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

DEFAULT_SYSTEM_PROMPT = (
    "Tu es un assistant médical francophone. "
    "Réponds de façon concise et précise."
)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Le champ 'message' est requis."}), 400

    history = data.get("messages", [])
    system_prompt = data.get("system_prompt", DEFAULT_SYSTEM_PROMPT)
    messages = (
        [{"role": "system", "content": system_prompt}]
        + list(history)
        + [{"role": "user", "content": message}]
    )

    def generate():
        with client.chat.stream(
            model="mistral-large-latest",
            messages=messages,
        ) as stream:
            for event in stream:
                content = event.data.choices[0].delta.content
                if content:
                    payload = json.dumps({"token": content})
                    yield f"data: {payload}\n\n"
        yield "data: [DONE]\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
