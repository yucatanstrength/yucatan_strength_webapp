
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tdee", methods=["POST"])
def calculate_tdee():
    data = request.get_json()
    gender = data["gender"]
    age = int(data["age"])
    height_cm = float(data["height_cm"])
    weight_kg = float(data["weight_kg"])
    activity = data["activity"]

    multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Active": 1.725,
        "Very Active": 1.9
    }

    if gender == "Male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    tdee = round(bmr * multipliers[activity])
    bmr = round(bmr)

    return jsonify({
        "tdee": tdee,
        "bmr": bmr,
        "multiplier": multipliers[activity],
        "activity": activity
    })

@app.route("/macros", methods=["POST"])
def calculate_macros():
    data = request.get_json()
    goal = data["goal"]
    tdee = int(data["tdee"])

    if goal == "Cut":
        calories = tdee - 500
    elif goal == "Bulk":
        calories = tdee + 500
    else:
        calories = tdee

    protein = round((1.0 * data["weight_kg"]) * 2.2)
    fats = round((0.4 * data["weight_kg"]) * 2.2)
    carbs = round((calories - (protein * 4 + fats * 9)) / 4)

    return jsonify({
        "calories": calories,
        "protein": protein,
        "fats": fats,
        "carbs": carbs
    })

if __name__ == "__main__":
    app.run(debug=True)
