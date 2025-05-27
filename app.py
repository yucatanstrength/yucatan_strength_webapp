
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tdee", methods=["POST"])
def tdee():
    data = request.get_json()
    gender = data["gender"]
    age = int(data["age"])
    height_cm = float(data["height"])
    weight_kg = float(data["weight"])
    activity = data["activity"]

    if gender == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    multiplier_map = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "Very Active": 1.9
    }

    multiplier = multiplier_map.get(activity, 1.2)
    tdee_val = round(bmr * multiplier)
    bmr = round(bmr)

    return jsonify({
        "tdee": tdee_val,
        "bmr": bmr,
        "multiplier": multiplier,
        "activity_label": activity,
        "cut": tdee_val - 500,
        "bulk": tdee_val + 500
    })

@app.route("/macros", methods=["POST"])
def macros():
    data = request.get_json()
    tdee = int(data["tdee"])
    goal = data["goal"]
    weight = float(data["weight"])
    gender = data["gender"]

    if goal == "cut":
        calories = tdee - 500
    elif goal == "bulk":
        calories = tdee + 500
    else:
        calories = tdee

    protein = round(weight * 1.1)
    fats = round((0.25 * calories) / 9)
    carbs = round((calories - (protein * 4 + fats * 9)) / 4)

    return jsonify({
        "calories": calories,
        "protein": protein,
        "fats": fats,
        "carbs": carbs
    })

if __name__ == "__main__":
    app.run(debug=True)
