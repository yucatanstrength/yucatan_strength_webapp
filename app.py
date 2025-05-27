from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def calculate_bmr(sex, weight_kg, height_cm, age):
    if sex == "Male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    elif sex == "Female":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    return 0

def calculate_tdee(bmr, activity_level):
    multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Active": 1.725,
        "Very Active": 1.9
    }
    return bmr * multipliers.get(activity_level, 1.2)

def calculate_macros(tdee, goal):
    if goal == "Cut":
        tdee -= 500
    elif goal == "Bulk":
        tdee += 500
    protein = round(tdee * 0.3 / 4)
    fats = round(tdee * 0.25 / 9)
    carbs = round((tdee - (protein * 4 + fats * 9)) / 4)
    return round(tdee), protein, fats, carbs

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    sex = data['sex']
    age = int(data['age'])
    height_cm = float(data['height_cm'])
    weight_kg = float(data['weight_kg'])
    activity = data['activity']
    goal = data['goal']
    bmr = calculate_bmr(sex, weight_kg, height_cm, age)
    tdee = calculate_tdee(bmr, activity)
    tdee, protein, fats, carbs = calculate_macros(tdee, goal)
    return jsonify({
        "tdee": tdee,
        "bmr": round(bmr),
        "protein": protein,
        "fats": fats,
        "carbs": carbs
    })

if __name__ == '__main__':
    app.run(debug=True)