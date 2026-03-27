from flask import Flask, render_template, request, jsonify
import secrets
import string

app = Flask(__name__)

def generate_password(length=16, use_upper=True, use_lower=True,
                      use_digits=True, use_symbols=True, exclude_ambiguous=False):
    charset = ""

    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?"

    if exclude_ambiguous:
        upper = upper.translate(str.maketrans("", "", "OI"))
        lower = lower.translate(str.maketrans("", "", "ol"))
        digits = digits.translate(str.maketrans("", "", "01"))

    if use_upper:   charset += upper
    if use_lower:   charset += lower
    if use_digits:  charset += digits
    if use_symbols: charset += symbols

    if not charset:
        return None, "Kam se kam ek option select karo!"

    # Ensure at least one char from each selected category
    guaranteed = []
    if use_upper:   guaranteed.append(secrets.choice(upper))
    if use_lower:   guaranteed.append(secrets.choice(lower))
    if use_digits:  guaranteed.append(secrets.choice(digits))
    if use_symbols: guaranteed.append(secrets.choice(symbols))

    remaining = length - len(guaranteed)
    if remaining < 0:
        remaining = 0
        guaranteed = guaranteed[:length]

    password_chars = guaranteed + [secrets.choice(charset) for _ in range(remaining)]

    # Shuffle securely
    for i in range(len(password_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

    return "".join(password_chars), None


def check_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:  score += 1
    if len(password) >= 12: score += 1
    if len(password) >= 16: score += 1

    if any(c.isupper() for c in password): score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in password): score += 1

    if score <= 2:
        return "Weak", "#ef5350", score
    elif score <= 4:
        return "Fair", "#ffa726", score
    elif score <= 5:
        return "Good", "#66bb6a", score
    else:
        return "Strong", "#00e5ff", score


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    try:
        length      = int(data.get('length', 16))
        use_upper   = bool(data.get('uppercase', True))
        use_lower   = bool(data.get('lowercase', True))
        use_digits  = bool(data.get('digits', True))
        use_symbols = bool(data.get('symbols', True))
        exclude_amb = bool(data.get('exclude_ambiguous', False))
        count       = min(int(data.get('count', 1)), 10)

        if not 4 <= length <= 128:
            return jsonify({'error': 'Length 4 se 128 ke beech hona chahiye'}), 400

        passwords = []
        for _ in range(count):
            pwd, err = generate_password(length, use_upper, use_lower,
                                         use_digits, use_symbols, exclude_amb)
            if err:
                return jsonify({'error': err}), 400
            strength, color, score = check_strength(pwd)
            passwords.append({'password': pwd, 'strength': strength,
                               'color': color, 'score': score})

        return jsonify({'passwords': passwords})

    except (ValueError, TypeError) as e:
        return jsonify({'error': 'Galat input: ' + str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
