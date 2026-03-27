# VANI — Python Voice Assistant

Ek Python Flask-based Voice Assistant jo Hindi aur English dono mein baat kar sakta hai.

## Tech Stack
- **Backend**: Python + Flask
- **AI**: Claude (Anthropic API)
- **TTS**: gTTS (Google Text-to-Speech) — Python se audio generate hota hai
- **STT**: Web Speech API (browser-based)
- **Frontend**: HTML + CSS + JavaScript

## Setup & Run

### 1. Python install karein
Python 3.8+ required hai.

### 2. Dependencies install karein
```bash
pip install -r requirements.txt
```

### 3. API Key set karein (optional)
Claude AI ke jawab ke liye:

**Windows:**
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

**Mac/Linux:**
```bash
export ANTHROPIC_API_KEY=your-api-key-here
```

API key nahi hai? App phir bhi kaam karega basic responses ke saath.

### 4. Server chalayein
```bash
python app.py
```

### 5. Browser mein open karein
```
http://localhost:5000
```

## Features
- 🎙️ Mic button dabayein ya **Spacebar** press karein
- ⌨️ Type karke bhi sawaal pooch sakte hain
- 🔊 Har jawab ke saath audio player aata hai (Python gTTS se)
- 🌐 Hindi aur English auto-detect
- 💻 Retro terminal design

## Files
```
vani-python/
├── app.py              ← Flask server + AI logic
├── requirements.txt    ← Python dependencies
├── README.md           ← Ye file
├── templates/
│   └── index.html      ← Frontend HTML
└── static/
    ├── style.css       ← Styling
    └── app.js          ← Voice + API logic
```
