from flask import Flask, render_template, request, jsonify
import json
import os
import re
import time
from difflib import SequenceMatcher

app = Flask(__name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.json")


def _read_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_data(obj):
    tmp_path = DATA_PATH + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, DATA_PATH)


def _normalize_text(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"[^\w\s]", " ", s, flags=re.UNICODE)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _as_list(v):
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x) for x in v if str(x).strip()]
    if isinstance(v, str):
        return [v] if v.strip() else []
    return [str(v)]


def _pick_reply(v):
    choices = _as_list(v)
    if not choices:
        return ""
    idx = int(time.time()) % len(choices)
    return choices[idx]


def _get_messages(data_obj):
    # Back-compat for existing typo "massages"
    msgs = data_obj.get("messages")
    if not isinstance(msgs, dict):
        msgs = data_obj.get("massages")
    if not isinstance(msgs, dict):
        return {}
    return msgs


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def _best_topic(user_msg_norm: str, data_obj: dict, keywords_map: dict):
    topics = [k for k in data_obj.keys() if k not in {"messages", "massages"}]
    topic_aliases = {t: set() for t in topics}

    for t in topics:
        topic_aliases[t].add(_normalize_text(t))

    for t, words in keywords_map.items():
        if t not in topic_aliases:
            continue
        for w in words:
            topic_aliases[t].add(_normalize_text(w))

    # Exact substring match (fast path)
    for t, aliases in topic_aliases.items():
        for a in aliases:
            if a and a in user_msg_norm:
                return t, 1.0, []

    # Fuzzy match
    scored = []
    for t, aliases in topic_aliases.items():
        best = 0.0
        for a in aliases:
            if not a:
                continue
            best = max(best, _similarity(user_msg_norm, a), _similarity(a, user_msg_norm))
        scored.append((best, t))

    scored.sort(reverse=True)
    best_score, best_topic = scored[0] if scored else (0.0, None)
    suggestions = [t for _, t in scored[1:4]]
    return best_topic, best_score, suggestions


data = _read_data()

# Keywords mapping
keywords = {
    "admission": ["admission", "apply", "enroll", "join"],
    "fees": ["fees", "fee", "payment", "cost"],
    "courses": ["courses", "branch", "stream", "program"],
    "hostel": ["hostel", "room", "stay"],
    "contact": ["contact", "phone", "number", "call"],
    "library": ["library", "books", "reading"],
    "sports": ["sports", "games", "play"],
    "faculty": ["faculty", "professor", "teacher"],
    "events": ["events", "fest", "cultural"],
    "placement": ["placement", "recruitment", "job"],
    "magazine": ["magazine", "publication", "newsletter"]
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global data
    payload = request.get_json(silent=True) or {}
    user_msg_raw = payload.get("message", "")
    user_msg_norm = _normalize_text(user_msg_raw)

    data = _read_data()
    msgs = _get_messages(data)

    # Small-talk intents
    if any(x in user_msg_norm for x in ["hello", "hi", "hey", "namaste", "hii", "hlo"]):
        reply = _pick_reply(msgs.get("greeting")) or "Hi! How can I help you?"
        return jsonify({"reply": reply, "topic": "greeting", "suggestions": ["admission", "fees", "courses", "hostel"]})
    if any(x in user_msg_norm for x in ["thanks", "thank you", "thx", "ty"]):
        reply = _pick_reply(msgs.get("thanks")) or "You're welcome!"
        return jsonify({"reply": reply, "topic": "thanks", "suggestions": []})
    if any(x in user_msg_norm for x in ["bye", "goodbye", "see you", "tata"]):
        reply = _pick_reply(msgs.get("farewell")) or "Goodbye! Take care!"
        return jsonify({"reply": reply, "topic": "farewell", "suggestions": []})

    topic, score, suggestions = _best_topic(user_msg_norm, data, keywords)
    if topic and score >= 0.55:
        reply = _pick_reply(data.get(topic)) or data.get("other") or "Is topic ka data abhi available nahi hai."
        return jsonify({"reply": reply, "topic": topic, "suggestions": []})

    # Fallback with suggestions
    if suggestions:
        return jsonify({
            "reply": "Mujhe samajh nahi aaya 😅 Kya aap inme se kisi topic ke baare me puch rahe ho?",
            "topic": None,
            "suggestions": suggestions
        })

    return jsonify({
        "reply": "Sorry 😅 Main admission, fees, courses, hostel, contact, placement, faculty, events, sports, library aur magazine ke questions best handle karta hoon.",
        "topic": None,
        "suggestions": ["admission", "fees", "courses", "hostel", "placement"]
    })


@app.route("/api/topics", methods=["GET"])
def list_topics():
    data_obj = _read_data()
    topics = sorted([k for k in data_obj.keys() if k not in {"messages", "massages"}])
    return jsonify({"topics": topics})


@app.route("/api/topic/<topic>", methods=["GET", "PUT", "DELETE"])
def topic_crud(topic):
    topic = (topic or "").strip()
    if not topic:
        return jsonify({"error": "Missing topic"}), 400

    data_obj = _read_data()

    if request.method == "GET":
        if topic not in data_obj:
            return jsonify({"error": "Not found"}), 404
        return jsonify({"topic": topic, "value": data_obj.get(topic)})

    if request.method == "DELETE":
        if topic in data_obj:
            del data_obj[topic]
            _write_data(data_obj)
        return jsonify({"ok": True})

    # PUT
    payload = request.get_json(silent=True) or {}
    value = payload.get("value", "")
    data_obj[topic] = value
    _write_data(data_obj)
    return jsonify({"ok": True})


@app.route("/admin")
def admin():
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
