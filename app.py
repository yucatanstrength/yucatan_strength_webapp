
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
    height = data.get("height")
    weight = data.get("weight")
    activity = data.get("activity")

    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    multiplier = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "Very Active": 1.9
    }.get(activity, 1.55)

    tdee = round(bmr * multiplier)
    return jsonify({"tdee": tdee})

@app.route("/macros", methods=["POST"])
def macros():
    data = request.get_json()
    tdee = data.get("tdee", 2500)
    goal = data.get("goal", "maintain")
    gender = data.get("gender", "male")
    weight_kg = data.get("weight", 75)
    weight_lb = weight_kg * 2.20462

    if goal == "cut":
        target_kcal = tdee * 0.75
    elif goal == "bulk":
        target_kcal = tdee * 1.10
    else:
        target_kcal = tdee

    if goal == "cut":
        protein_g = weight_lb * 1.3
    elif goal == "bulk":
        protein_g = weight_lb * 0.9
    else:
        protein_g = weight_lb * 1.1

    if goal == "cut":
        fat_g = weight_lb * 0.35
    elif goal == "bulk":
        fat_g = weight_lb * 0.5
    else:
        fat_g = weight_lb * 0.4

    kcal_protein = protein_g * 4
    kcal_fat = fat_g * 9
    kcal_remaining = target_kcal - (kcal_protein + kcal_fat)
    carb_g = max(kcal_remaining / 4, 0)

    return jsonify({
        "calories": int(target_kcal),
        "protein": int(protein_g),
        "fats": int(fat_g),
        "carbs": int(carb_g)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
