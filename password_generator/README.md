# 🔐 PassForge — Password Generator (Python Flask)

## Features 
-✅ Cryptographically secure (uses Python secrets module).

-✅ Password length: 4 to 128 characters.

-✅ Toggle options: Uppercase, Lowercase, Numbers, Symbols.

-✅ Option to exclude ambiguous characters (O, 0, I, l, 1).

-✅ Generate 1–10 passwords at once.

-✅ Password strength indicator (Weak / Fair / Good / Strong).

-✅ One-click copy button.

-✅ Copy all generated passwords at once

---

## Setup & Run 

```bash
# Step 1 — folder mein jao
cd password_generator

# Step 2 — dependencies install karo
pip install -r requirements.txt

# Step 3 — app chalao
python app.py

# Step 4 — browser mein kholo
http://127.0.0.1:5000
```

---

## Project Structure
```
password_generator/
├── app.py              ← Flask backend + password logic
├── requirements.txt    ← Dependencies (sirf flask)
├── README.md           ← Ye file
└── templates/
    └── index.html      ← Frontend UI
```

---

## Security Note
This application uses Python’s secrets module, which is more secure than the random module. It generates cryptographically strong random values, making the generated passwords safer for real-world use.
