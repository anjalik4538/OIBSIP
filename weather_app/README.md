# 🌤️  Weather App (Python Flask)

## ✅ No API Key Required!
This application uses the free API from Open-Meteo, which does not require any registration or API key.

---

## Features 
- 🌍 Duniya ke kisi bhi shehar ka mausam
- 🌡️ Temperature, Feels Like, Humidity, Wind
- 🗓️ 7-din ka forecast
- 🌙 Din/Raat ke hisaab se animated sky background
- 🧭 Wind direction compass
- ☔ Rain probability bar
- 🏙️ Quick city buttons (Delhi, Mumbai, Raipur, etc.)

---

## Setup & Run 

```bash
# Step 1 — folder mein jao
cd weather_app

# Step 2 — Flask install karo
pip install -r requirements.txt

# Step 3 — App chalao
python app.py

# Step 4 — Browser mein kholo
http://127.0.0.1:5000
```

> ⚠️ Internet connection zaroori hai (weather data fetch karne ke liye)

---

## Project Structure
```
weather_app/
├── app.py              ← Flask backend + Open-Meteo API calls
├── requirements.txt    ← Sirf Flask (koi extra library nahi)
├── README.md           ← Ye file
└── templates/
    └── index.html      ← Full frontend (HTML + CSS + JS)
```

---

## APIs Used
| API | Purpose | Cost |
|-----|---------|------|
| Open-Meteo Geocoding | City → Lat/Lon | FREE |
| Open-Meteo Forecast  | Weather data   | FREE |
