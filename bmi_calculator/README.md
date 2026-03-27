# 🏥 BMI Calculator — Python Flask App

## Features / विशेषताएं
- ✅ Metric (kg/cm) aur Imperial (lbs/inches) dono support
- ✅ Live animated BMI gauge/scale
- ✅ Ideal weight range calculation
- ✅ 4 categories: Underweight, Normal, Overweight, Obese
- ✅ Hindi mein advice
- ✅ Beautiful warm editorial design

---

## Setup & Run / चलाने का तरीका

### Step 1 — Dependencies install karo
```bash
cd bmi_calculator
pip install -r requirements.txt
```

### Step 2 — App chalao
```bash
python app.py
```

### Step 3 — Browser mein kholo
```
http://127.0.0.1:5000
```

---

## BMI Categories
| BMI Range | Category |
|-----------|----------|
| < 18.5 | Underweight |
| 18.5 – 24.9 | Normal Weight ✅ |
| 25.0 – 29.9 | Overweight |
| ≥ 30.0 | Obese |

---

## Project Structure
```
bmi_calculator/
├── app.py              ← Flask backend + BMI logic
├── requirements.txt    ← Python dependencies
├── README.md           ← Ye file
└── templates/
    └── index.html      ← Frontend UI
```
