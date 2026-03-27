"""
VANI Voice Assistant — Python Flask Backend
===========================================

Installation:
    pip install flask anthropic gtts

Run:
    python app.py

Then open in browser: http://localhost:5000
"""

import os
import tempfile
from flask import Flask, render_template, request, jsonify, send_file
from gtts import gTTS
import anthropic

app = Flask(__name__)

# ── Anthropic Client Setup ───────────────────────────────
# Set your API key as environment variable:
# Windows (PowerShell):
# $env:ANTHROPIC_API_KEY="your_api_key_here"

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY", "")
)

# System Prompt (AI Behavior)
SYSTEM_PROMPT = """You are VANI — a helpful and friendly voice assistant.

Respond in the same language as the user (Hindi or English).
Keep responses short and conversational (2-4 sentences max).
Use a friendly and natural tone, not formal.
Do not use emojis since responses will be spoken aloud.
"""

# ── Home Route ───────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# ── Chat API (AI Response) ───────────────────────────────
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_text = data.get("text", "").strip()

    if not user_text:
        return jsonify({"error": "Text is empty"}), 400

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")

    # If no API key → use fallback
    if not api_key:
        reply = get_fallback_response(user_text)
    else:
        try:
            message = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=300,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_text}],
            )
            reply = message.content[0].text
        except Exception:
            reply = get_fallback_response(user_text)

    return jsonify({"reply": reply})


# ── Text-to-Speech API ───────────────────────────────────
@app.route("/api/tts", methods=["POST"])
def text_to_speech():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Text is empty"}), 400

    try:
        # Auto-detect language
        english_chars = sum(1 for c in text if ord(c) < 128 and c.isalpha())
        total_chars = sum(1 for c in text if c.isalpha())

        if total_chars > 0 and english_chars / total_chars > 0.7:
            lang = "en"
        else:
            lang = "hi"

        tts = gTTS(text=text, lang=lang, slow=False)

        tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        tts.save(tmp.name)
        tmp.close()

        return send_file(
            tmp.name,
            mimetype="audio/mpeg",
            as_attachment=False,
            download_name="speech.mp3",
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Fallback Responses (No API Key) ──────────────────────
def get_fallback_response(text):
    t = text.lower()

    if any(w in t for w in ["hello", "hi", "hey"]):
        return "Hello! I am VANI. How are you? How can I assist you today?"

    if any(w in t for w in ["name", "who are you"]):
        return "My name is VANI, your AI voice assistant. How can I help you?"

    if any(w in t for w in ["time"]):
        from datetime import datetime
        return f"The current time is {datetime.now().strftime('%I:%M %p')}."

    if any(w in t for w in ["date", "today"]):
        from datetime import datetime
        return f"Today's date is {datetime.now().strftime('%d %B %Y')}."

    if any(w in t for w in ["joke", "funny"]):
        return "Why do programmers prefer dark mode? Because light attracts bugs!"

    if any(w in t for w in ["thanks", "thank you"]):
        return "You're welcome! Happy to help."

    if any(w in t for w in ["bye"]):
        return "Goodbye! Take care."

    return "I'm currently running in limited mode. Please set the ANTHROPIC_API_KEY for full functionality."


# ── Run Server ───────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("   VANI Voice Assistant Server Running")
    print("   Open: http://localhost:5000")
    print("=" * 50)

    app.run(debug=True, port=5000)