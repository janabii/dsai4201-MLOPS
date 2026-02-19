# support_bot/core.py
import re
import uuid
from typing import Dict, List, Optional, Tuple

from mistral_client import mistral
from prompts import INTENT_PROMPT, RESPONSE_PROMPT, SUMMARY_PROMPT


ALLOWED_INTENTS = {
    "card arrival",
    "change pin",
    "exchange rate",
    "country support",
    "cancel transfer",
    "charge dispute",
    "customer service",
}

# In-memory session store: {session_id: [{"role":"user"/"assistant","content":"..."}]}
SESSIONS: Dict[str, List[Dict[str, str]]] = {}


def _normalize_intent(text: str) -> str:
    t = (text or "").strip().lower()
    if t in ALLOWED_INTENTS:
        return t
    for label in ALLOWED_INTENTS:
        if label in t:
            return label
    return "customer service"


def classify_intent(inquiry: str) -> str:
    raw = mistral(INTENT_PROMPT.format(inquiry=inquiry), model="mistral-small-latest")
    return _normalize_intent(raw)


def extract_name(inquiry: str) -> Optional[str]:
    patterns = [
        r"\bmy name is\s+([A-Z][a-zA-Z'-]{1,30})\b",
        r"\bi am\s+([A-Z][a-zA-Z'-]{1,30})\b",
        r"\bi'm\s+([A-Z][a-zA-Z'-]{1,30})\b",
    ]
    for p in patterns:
        m = re.search(p, inquiry)
        if m:
            return m.group(1)
    return None


def format_history(history: List[Dict[str, str]], max_turns: int = 12) -> str:
    trimmed = history[-max_turns:]
    lines = []
    for turn in trimmed:
        role = turn.get("role", "user").upper()
        content = turn.get("content", "")
        lines.append(f"{role}: {content}")
    return "\n".join(lines).strip() if lines else "(no prior messages)"


def get_session(session_id: Optional[str]) -> Tuple[str, List[Dict[str, str]]]:
    if not session_id:
        session_id = str(uuid.uuid4())
    history = SESSIONS.setdefault(session_id, [])
    return session_id, history


def generate_response(inquiry: str, intent: str, history: List[Dict[str, str]], name: Optional[str]) -> str:
    prompt = RESPONSE_PROMPT.format(
        name=name or "not provided",
        intent=intent,
        history=format_history(history),
        inquiry=inquiry,
    )
    return mistral(prompt, model="mistral-small-latest").strip()


def chat(session_id: Optional[str], inquiry: str) -> Dict[str, str]:
    session_id, history = get_session(session_id)

    name = extract_name(inquiry)
    intent = classify_intent(inquiry)

    history.append({"role": "user", "content": inquiry})
    reply = generate_response(inquiry, intent, history, name=name)
    history.append({"role": "assistant", "content": reply})

    return {"session_id": session_id, "intent": intent, "response": reply}


def summarize(session_id: str) -> Dict[str, str]:
    history = SESSIONS.get(session_id, [])
    if not history:
        return {"session_id": session_id, "summary": "- No conversation yet."}

    prompt = SUMMARY_PROMPT.format(history=format_history(history, max_turns=50))
    summary = mistral(prompt, model="mistral-small-latest").strip()
    return {"session_id": session_id, "summary": summary}
