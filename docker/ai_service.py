"""
Flask AI Service — Chat Bridge

This microservice sits between your Django app (careflow_app) and your
Ollama instance (localgen_brain). It exposes a single POST endpoint so
that Django never needs to talk to Ollama directly.

Environment variables you can set at runtime:
  OLLAMA_URL   – default: http://localgen_brain:11434
  OLLAMA_MODEL – default: gemma2:4b
"""

import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localgen_brain:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma2:4b")


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Accepts:  { "model": "...", "messages": [ { "role": "...", "content": "..." }, ... ], "stream": False }
    Returns:  { "message": { "role": "assistant", "content": "..." }, "eval_count": 123 }
    """
    data = request.get_json(silent=True) or {}
    
    # Django sends 'messages' (list) and 'model' (string)
    messages = data.get("messages", [])
    model = data.get("model", OLLAMA_MODEL)
    stream = data.get("stream", False)

    if not messages:
        return jsonify({"error": "messages list is required"}), 400

    print(f"Incoming request to bridge: model={model}, messages_count={len(messages)}")

    # Build the payload Ollama /api/chat expects
    ollama_payload = {
        "model": model,
        "messages": messages,
        "stream": stream,
    }

    try:
        print(f"Forwarding request to Ollama at {OLLAMA_URL}/api/chat")
        resp = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json=ollama_payload,
            timeout=300,  # LLMs can be slow (5 min)
        )
        resp.raise_for_status()
        result = resp.json()
        
        # Ollama /api/chat returns { "message": { "role": "assistant", "content": "..." }, "done": true, "total_duration": ... }
        # We return it as is to match Django's expectations
        return jsonify(result)
        
    except requests.exceptions.ConnectionError:
        print(f"ConnectionError: Could not reach Ollama at {OLLAMA_URL}")
        return jsonify({"error": f"Could not reach Ollama at {OLLAMA_URL}"}), 502
    except requests.exceptions.Timeout:
        print(f"TimeoutError: Ollama request timed out")
        return jsonify({"error": "Ollama request timed out"}), 504
    except Exception as exc:
        print(f"Unexpected error: {str(exc)}")
        return jsonify({"error": str(exc)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "ollama_url": OLLAMA_URL, "model": OLLAMA_MODEL})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
