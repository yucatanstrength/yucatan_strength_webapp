
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def calculate_bmr(sex, weight_kg, height_cm, age):
    if sex == "Male":
        return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

def calculate_tdee(bmr, activity_level):
    multipliers = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.725,
        "Very Active": 1.9
    }
    return bmr * multipliers.get(activity_level, 1.2)

def calculate_macros(tdee, goal):
    if goal == "Cut":
        tdee -= 500
    elif goal == "Bulk":
        tdee += 500
    protein = round(0.9 * tdee / 4)
    fats = round(0.3 * tdee / 9)
    carbs = round((tdee - (protein * 4 + fats * 9)) / 4)
    return round(tdee), protein, fats, carbs

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tdee", methods=["POST"])
def tdee():
    data = request.json
    bmr = calculate_bmr(data["sex"], data["weight_kg"], data["height_cm"], data["age"])
    tdee = calculate_tdee(bmr, data["activity"])
    return jsonify({
        "bmr": round(bmr),
        "tdee": round(tdee),
        "cut": round(tdee - 500),
        "bulk": round(tdee + 500)
    })

@app.route("/macros", methods=["POST"])
def macros():
    data = request.json
    tdee = data["tdee"]
    goal = data["goal"]
    tdee, protein, fats, carbs = calculate_macros(tdee, goal)
    return jsonify({
        "calories": tdee,
        "protein": protein,
        "fats": fats,
        "carbs": carbs
    })
