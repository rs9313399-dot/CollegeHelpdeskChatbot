from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load data
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

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
    user_msg = request.json.get("message", "").lower()

    for key, words in keywords.items():
        for w in words:
            if w in user_msg:
                return jsonify({
                    "reply": data.get(
                        key,
                        "Is topic ka data abhi available nahi hai bhai 😅"
                    )
                })

    return jsonify({
        "reply": "Sorry bhai 😅 main admission, fees, courses, hostel, contact, placement, faculty, events, sports, library aur magazine ke questions hi samajhta hoon"
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
