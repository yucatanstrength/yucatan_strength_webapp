
document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('select, input');

    inputs.forEach(input => input.addEventListener('change', calculateAll));

    function calculateAll() {
        const gender = document.getElementById("gender").value;
        const age = document.getElementById("age").value;
        const height_cm = document.getElementById("height_cm").value;
        const weight_kg = document.getElementById("weight_kg").value;
        const activity = document.getElementById("activity").value;
        const goal = document.getElementById("goal").value;

        fetch('/tdee', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({gender, age, height_cm, weight_kg, activity})
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById("tdee-output").textContent = `TDEE: ${data.tdee} kcal`;
            document.getElementById("bmr-output").textContent = `BMR: ${data.bmr} kcal`;
            document.getElementById("activity-output").textContent = `Activity Multiplier: ${data.multiplier} (${data.activity})`;

            fetch('/macros', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    goal,
                    weight_kg,
                    tdee: data.tdee
                })
            })
            .then(res => res.json())
            .then(macro => {
                document.getElementById("macro-output").innerHTML = `
                    Calories: ${macro.calories}<br>
                    Protein: ${macro.protein}g<br>
                    Fats: ${macro.fats}g<br>
                    Carbs: ${macro.carbs}g
                `;
            });
        });
    }

    calculateAll(); // Initial load
});
