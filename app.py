
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tdee", methods=["POST"])
def tdee():
    data = request.json
    gender = data.get("gender")
    age = int(data.get("age"))
    height = float(data.get("height_cm"))
    weight = float(data.get("weight_kg"))
    activity = data.get("activity")

    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    multiplier = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.725,
        "Very Active": 1.9
    }[activity]

    tdee_value = int(bmr * multiplier)
    return jsonify({"tdee": tdee_value})

@app.route("/macros", methods=["POST"])
def macros():
    data = request.json
    tdee = int(data.get("tdee"))
    goal = data.get("goal")

    if goal == "Cut":
        tdee -= 500
    elif goal == "Bulk":
        tdee += 500

    protein = int((0.33 * tdee) / 4)
    fats = int((0.25 * tdee) / 9)
    carbs = int((tdee - (protein * 4 + fats * 9)) / 4)

    return jsonify({"calories": tdee, "protein": protein, "fats": fats, "carbs": carbs})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
