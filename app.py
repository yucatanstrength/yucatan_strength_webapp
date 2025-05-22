
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tdee", methods=["POST"])
def tdee():
    data = request.get_json()
    gender = data.get("gender")
    age = data.get("age")
    height = data.get("height")  # in cm
    weight = data.get("weight")  # in kg
    activity = data.get("activity")

    # BMR (Mifflin-St Jeor)
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    multiplier = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }.get(activity, 1.55)

    tdee = round(bmr * multiplier)
    return jsonify({"tdee": tdee})

@app.route("/macros", methods=["POST"])
def macros():
    data = request.get_json()
    tdee = data.get("tdee", 2500)
    goal = data.get("goal", "maintain")

    if goal == "cut":
        tdee -= 500
    elif goal == "bulk":
        tdee += 250

    protein = round((0.8 * tdee) / 4)
    fats = round((0.25 * tdee) / 9)
    carbs = round((tdee - (protein * 4 + fats * 9)) / 4)

    return jsonify({
        "calories": round(tdee),
        "protein": protein,
        "fats": fats,
        "carbs": carbs
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
