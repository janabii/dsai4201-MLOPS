# support_bot/api.py
from flask import Flask, jsonify, request
from core import chat, summarize

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/chat")
def chat_route():
    data = request.get_json(force=True) or {}
    inquiry = (data.get("inquiry") or "").strip()
    session_id = data.get("session_id")

    if not inquiry:
        return jsonify({"error": "Missing 'inquiry'"}), 400

    return jsonify(chat(session_id=session_id, inquiry=inquiry))


@app.get("/summary/<session_id>")
def summary_route(session_id: str):
    return jsonify(summarize(session_id))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
