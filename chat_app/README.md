# 🌐 NeonChat — Browser-Based Chat Application

## Features 
- ✅ Real-time messaging with WebSockets (Socket.IO)
- ✅ Multiple chat rooms: #general, #tech, #random, #hindi
- ✅ Typing indicators (live)
- ✅ Online users list with avatars
- ✅ Beautiful dark neon UI design
- ✅ Toast notifications on join/leave
- ✅ Hindi language friendly

---

## Setup & Run 

### Step 1 —  Install Python (3.8+)
https://python.org/downloads se Python download karo

### Step 2 —  Install Dependencies
```bash
cd chat_app
pip install -r requirements.txt
```

### Step 3 — Run App
```bash
python app.py
```

### Step 4 — Open Browser 
```
http://localhost:5000
```

---

## Multiple Users Test karne ke liye
- Ek hi computer pe multiple browser tabs kholo
- Ya alag device pe `http://[YOUR_IP]:5000` kholo
- Apna IP jaanne ke liye: `ipconfig` (Windows) ya `ifconfig` (Mac/Linux)

---

## Project Structure
```
chat_app/
├── app.py              ← Flask + SocketIO server
├── requirements.txt    ← Python dependencies
├── README.md           ← Ye file
└── templates/
    └── index.html      ← Frontend (HTML/CSS/JS)
```

---

## Tech Stack
- **Backend**: Python, Flask, Flask-SocketIO
- **Frontend**: Vanilla JS, Socket.IO client
- **Real-time**: WebSockets (via eventlet)
