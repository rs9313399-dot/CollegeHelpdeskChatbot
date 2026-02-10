from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

keywords = {
    "admission": ["admission", "apply", "enroll", "join"],
    "fees": ["fees", "fee", "payment", "cost"],
    "courses": ["courses", "branch", "stream", "program"],
    "hostel": ["hostel", "room", "stay"],
    "contact": ["contact", "phone", "number", "call"]
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"].lower()

    for key, words in keywords.items():
        for w in words:
            if w in user_msg:
                return jsonify({"reply": data[key]})

    return jsonify({
        "reply": "Sorry bhai 😅 main sirf admission, fees, courses, hostel aur contact ka jawab deta hoon"
    })

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
