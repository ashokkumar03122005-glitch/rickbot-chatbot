from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# === OpenRouter API Key ===
OPENROUTER_API_KEY = ""
SITE_URL = "https://example.com"
SITE_NAME = "MyRickBotSite"

# === RickBot personality ===
RICKBOT_PROMPT = """
You are RickBot, a sarcastic drunk genius like Rick Sanchez from Rick and Morty.
Always reply in **short, concise, funny sentences** suitable for real-time speech.
Keep replies under 30 words.
"""


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    # === Prepare payload for OpenRouter GPT-4.1 API ===
    payload = {
        "model": "openai/gpt-4.1",
        "max_tokens": 60,  # adjust based on your credits
        "messages": [
            {"role": "system", "content": RICKBOT_PROMPT},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": SITE_URL,
                "X-Title": SITE_NAME
            },
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            data = response.json()
            text = data["choices"][0]["message"]["content"]
            return jsonify({"reply": text})
        else:
            return jsonify({"error": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
