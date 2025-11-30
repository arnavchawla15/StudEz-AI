from flask import Flask, request, jsonify
from flask_cors import CORS
from studezz_ai import ask_ai   # this imports your chatbot function

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    msg = data.get("message", "").strip()
    if not msg:
        return jsonify({"error": "empty message"}), 400
    try:
        reply = ask_ai(msg)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
