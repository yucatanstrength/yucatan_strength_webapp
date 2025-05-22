from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import math, os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

# Placeholder for all calculator routes

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


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
    preference = data['preference']

    if goal == 'cut':
        tdee -= 500
    elif goal == 'bulk':
        tdee += 500

    if preference == 'balanced':
        protein_ratio, fat_ratio = 0.3, 0.25
    elif preference == 'high_protein':
        protein_ratio, fat_ratio = 0.4, 0.2
    elif preference == 'high_carb':
        protein_ratio, fat_ratio = 0.25, 0.2
    else:
        protein_ratio, fat_ratio = 0.3, 0.25

    protein = round((tdee * protein_ratio) / 4)
    fats = round((tdee * fat_ratio) / 9)
    carbs = round((tdee - (protein * 4 + fats * 9)) / 4)

    return jsonify({'calories': tdee, 'protein': protein, 'fats': fats, 'carbs': carbs})
