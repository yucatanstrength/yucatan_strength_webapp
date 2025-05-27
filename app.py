from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

def calculate_bmr(sex, weight_kg, height_cm, age):
    if sex == "Male":
        return int((10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5)
    else:
        return int((10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161)

activity_multipliers = {
    "Sedentary": 1.2,
    "Lightly active": 1.375,
    "Moderately active": 1.55,
    "Active": 1.725,
    "Very active": 1.9
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    sex = data["sex"]
    age = int(data["age"])
    weight_lbs = int(data["weight"])
    height_inches = int(data["height"])
    activity = data["activity"]

    weight_kg = weight_lbs * 0.453592
    height_cm = height_inches * 2.54

    bmr = calculate_bmr(sex, weight_kg, height_cm, age)
    multiplier = activity_multipliers[activity]
    tdee = int(bmr * multiplier)

    return jsonify({
        "tdee": tdee,
        "bmr": bmr,
        "activity": activity,
        "multiplier": multiplier
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)