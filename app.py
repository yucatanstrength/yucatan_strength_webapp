from flask import Flask, render_template, request, jsonify
import math
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Calculators...

@app.route("/")
def home():
    return render_template("index.html")

# Placeholder routes...
@app.route("/tdee", methods=["POST"])
def tdee():
    return jsonify({"tdee": 3000})

@app.route("/macros", methods=["POST"])
def macros():
    return jsonify({"protein": 180, "fats": 70, "carbs": 310})

if __name__ == "__main__":
    import os; app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
