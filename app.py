
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

def calculate_bmr(sex, weight_kg, height_cm, age):
    if sex == 'male':
        return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

@app.route("/calculate_tdee", methods=["POST"])
def calculate_tdee():
    data = request.json
    sex = data["sex"]
    age = int(data["age"])
    weight = float(data["weight"])
    height = float(data["height"])
    activity = float(data["activity"])

    # Convert lbs to kg and inches to cm
    weight_kg = weight * 0.453592
    height_cm = height * 2.54

    bmr = calculate_bmr(sex, weight_kg, height_cm, age)
    tdee = round(bmr * activity)
    bmr = round(bmr)

    return jsonify({"tdee": tdee, "bmr": bmr})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
