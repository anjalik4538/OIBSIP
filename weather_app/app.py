from flask import Flask, render_template, request, jsonify
import urllib.request
import urllib.parse
import json

app = Flask(__name__)

# Open-Meteo — FREE, no API key needed!
GEO_URL    = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WMO_CODES = {
    0:  ("Clear Sky",           "☀️"),
    1:  ("Mainly Clear",        "🌤️"),
    2:  ("Partly Cloudy",       "⛅"),
    3:  ("Overcast",            "☁️"),
    45: ("Foggy",               "🌫️"),
    48: ("Icy Fog",             "🌫️"),
    51: ("Light Drizzle",       "🌦️"),
    53: ("Drizzle",             "🌦️"),
    55: ("Heavy Drizzle",       "🌧️"),
    61: ("Slight Rain",         "🌧️"),
    63: ("Rain",                "🌧️"),
    65: ("Heavy Rain",          "🌧️"),
    71: ("Slight Snow",         "🌨️"),
    73: ("Snow",                "❄️"),
    75: ("Heavy Snow",          "❄️"),
    77: ("Snow Grains",         "🌨️"),
    80: ("Rain Showers",        "🌦️"),
    81: ("Rain Showers",        "🌧️"),
    82: ("Violent Showers",     "🌧️"),
    85: ("Snow Showers",        "🌨️"),
    86: ("Heavy Snow Showers",  "❄️"),
    95: ("Thunderstorm",        "⛈️"),
    96: ("Thunderstorm + Hail", "⛈️"),
    99: ("Thunderstorm + Hail", "⛈️"),
}

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "WeatherApp/1.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode())

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weather")
def weather():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "City name likhna zaroori hai"}), 400

    # Step 1: Geocode
    geo_params = urllib.parse.urlencode({"name": city, "count": 1, "language": "en", "format": "json"})
    try:
        geo = fetch_json(f"{GEO_URL}?{geo_params}")
    except Exception:
        return jsonify({"error": "Geocoding API se connect nahi ho paya"}), 502

    results = geo.get("results")
    if not results:
        return jsonify({"error": f"'{city}' nahi mila. Dusra naam try karo."}), 404

    place = results[0]
    lat   = place["latitude"]
    lon   = place["longitude"]
    name  = place.get("name", city)
    country = place.get("country", "")
    admin1  = place.get("admin1", "")

    # Step 2: Weather
    params = urllib.parse.urlencode({
        "latitude": lat,
        "longitude": lon,
        "current": ",".join([
            "temperature_2m", "apparent_temperature", "relative_humidity_2m",
            "wind_speed_10m", "wind_direction_10m", "weather_code",
            "surface_pressure", "visibility", "is_day"
        ]),
        "daily": ",".join([
            "weather_code", "temperature_2m_max", "temperature_2m_min",
            "precipitation_probability_max", "wind_speed_10m_max"
        ]),
        "timezone": "auto",
        "forecast_days": 7
    })
    try:
        data = fetch_json(f"{WEATHER_URL}?{params}")
    except Exception:
        return jsonify({"error": "Weather API se data nahi aaya"}), 502

    cur  = data["current"]
    daily = data["daily"]

    wcode     = cur.get("weather_code", 0)
    desc, icon = WMO_CODES.get(wcode, ("Unknown", "🌡️"))

    # Build 7-day forecast
    forecast = []
    days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
    for i, date_str in enumerate(daily["time"]):
        import datetime
        d = datetime.date.fromisoformat(date_str)
        dc, di = WMO_CODES.get(daily["weather_code"][i], ("Unknown","🌡️"))
        forecast.append({
            "day":       days[d.weekday()] if i > 0 else "Today",
            "date":      d.strftime("%d %b"),
            "icon":      di,
            "desc":      dc,
            "max":       round(daily["temperature_2m_max"][i]),
            "min":       round(daily["temperature_2m_min"][i]),
            "rain_pct":  daily["precipitation_probability_max"][i],
            "wind":      round(daily["wind_speed_10m_max"][i]),
        })

    # Wind direction label
    wd = cur.get("wind_direction_10m", 0)
    dirs = ["N","NE","E","SE","S","SW","W","NW"]
    wind_dir = dirs[round(wd / 45) % 8]

    return jsonify({
        "city":        name,
        "region":      admin1,
        "country":     country,
        "lat":         round(lat, 2),
        "lon":         round(lon, 2),
        "temp":        round(cur["temperature_2m"]),
        "feels_like":  round(cur["apparent_temperature"]),
        "humidity":    cur["relative_humidity_2m"],
        "wind_speed":  round(cur["wind_speed_10m"]),
        "wind_dir":    wind_dir,
        "pressure":    round(cur.get("surface_pressure", 0)),
        "visibility":  round(cur.get("visibility", 0) / 1000, 1),
        "description": desc,
        "icon":        icon,
        "is_day":      cur.get("is_day", 1),
        "forecast":    forecast,
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
