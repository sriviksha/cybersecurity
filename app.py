from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({
            "result": "Please enter a message to check."
        }), 400

    text = message.lower()
    warnings = []

    patterns = {
        "Urgent or threatening language": [
            r"\bimmediately\b", r"\burgent\b",
            r"\barrest\b", r"\bpolice\b",
            r"\baccount blocked\b"
        ],
        "Requests for money or secret codes": [
            r"\botp\b", r"\bpassword\b",
            r"\btransfer money\b", r"\bpay now\b"
        ],
        "Suspicious links": [
            r"https?://", r"\bbit\.ly\b"
        ],
        "Possible misinformation": [
            r"\bshare immediately\b",
            r"\bshocking news\b",
            r"\b100% confirmed\b"
        ]
    }

    for label, expressions in patterns.items():
        if any(re.search(pattern, text) for pattern in expressions):
            warnings.append(label)

    if warnings:
        result = (
            "Caution: this message contains suspicious signs. "
            "Verify it using trusted, official sources."
        )
    else:
        result = (
            "No listed warning pattern was detected. "
            "This does not prove the message is safe or true."
        )

    return jsonify({
        "result": result,
        "warnings": warnings
    })

if __name__ == "__main__":
    app.run(debug=True)