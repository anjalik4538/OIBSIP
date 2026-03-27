from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)

def get_category(bmi):
    if bmi < 18.5:
        return "Underweight", "Aapka weight thoda kam hai. Balanced diet lein.", "#64b5f6", "underweight"
    elif bmi < 25.0:
        return "Normal Weight", "Bahut badhiya! Aap healthy range mein hain.", "#66bb6a", "normal"
    elif bmi < 30.0:
        return "Overweight", "Thoda weight kam karna beneficial hoga.", "#ffa726", "overweight"
    else:
        return "Obese", "Doctor se mil ke diet aur exercise plan banayein.", "#ef5350", "obese"

def ideal_weight_range(height_cm):
    h = height_cm / 100
    low = round(18.5 * h * h, 1)
    high = round(24.9 * h * h, 1)
    return low, high

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    try:
        weight = float(data['weight'])
        height = float(data['height'])
        unit = data.get('unit', 'metric')

        if unit == 'imperial':
            # lbs to kg, inches to cm
            weight = weight * 0.453592
            height = height * 2.54

        if weight <= 0 or height <= 0:
            return jsonify({'error': 'Valid values daalo'}), 400
        if weight > 500 or height > 300 or height < 50:
            return jsonify({'error': 'Values range se bahar hain'}), 400

        bmi = calculate_bmi(weight, height)
        category, advice, color, key = get_category(bmi)
        ideal_low, ideal_high = ideal_weight_range(height)

        # BMI scale position (10 to 40 range mapped to 0-100%)
        position = max(0, min(100, (bmi - 10) / 30 * 100))

        return jsonify({
            'bmi': bmi,
            'category': category,
            'advice': advice,
            'color': color,
            'key': key,
            'ideal_low': ideal_low,
            'ideal_high': ideal_high,
            'position': round(position, 1)
        })
    except (KeyError, ValueError, TypeError):
        return jsonify({'error': 'Galat input hai'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
