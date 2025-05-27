
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
    gender = data.get("gender")
    age = int(data.get("age"))
    height_cm = float(data.get("height_cm"))
    weight_kg = float(data.get("weight_kg"))
    activity_level = data.get("activity_level")

    # Activity multipliers
    multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Active": 1.725,
        "Very Active": 1.9
    }

    # BMR calculation using Mifflin-St Jeor
    if gender == "Male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    tdee_value = int(bmr * multipliers[activity_level])
    return jsonify({"tdee": tdee_value})

if __name__ == "__main__":
    app.run(debug=True)
