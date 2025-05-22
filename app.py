
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import math
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tdee', methods=['POST'])
def tdee():
    data = request.json
    weight = data['weight']
    height = data['height']
    age = data['age']
    gender = data['gender']
    activity = data['activity']

    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    multiplier = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    tdee_val = round(bmr * multiplier.get(activity, 1.2), 2)
    return jsonify({'tdee': tdee_val})

@app.route('/macros', methods=['POST'])
def macros():
    data = request.json
    tdee = data['tdee']
    goal = data['goal']
    if goal == 'cut':
        tdee -= 500
    elif goal == 'bulk':
        tdee += 500
    protein = round(tdee * 0.3 / 4)
    fats = round(tdee * 0.25 / 9)
    carbs = round((tdee - (protein * 4 + fats * 9)) / 4)
    return jsonify({'calories': tdee, 'protein': protein, 'fats': fats, 'carbs': carbs})

@app.route('/healthscore', methods=['POST'])
def healthscore():
    data = request.json
    weight = data['weight']
    height = data['height']
    waist = data['waist']
    hips = data['hips']
    sleep = data['sleep']
    water = data['water']
    hrv = data['hrv']
    mood = data['mood']

    bmi = weight / ((height / 100) ** 2)
    whr = waist / hips
    sleep_score = min(sleep / 8, 1)
    water_score = min(water / (weight * 0.035), 1)
    hrv_score = max(min(hrv / 100, 1), 0.5)
    mental_score = mood / 10

    raw_score = (1 / bmi) * 5 + (1 - whr) * 30 + sleep_score * 20 + water_score * 10 + hrv_score * 15 + mental_score * 20
    final_score = max(min(round(raw_score, 2), 100), 0)

    # Tier logic
    if final_score < 40:
        tier = "Armadillo 🦥"
    elif final_score < 60:
        tier = "Spider Monkey 🐒"
    elif final_score < 80:
        tier = "Jaguar 🐆"
    elif final_score < 95:
        tier = "Eagle 🦅"
    else:
        tier = "WARRIOR ⚔️"

    return jsonify({'score': final_score, 'tier': tier})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
