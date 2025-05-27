document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('select, input');
    inputs.forEach(input => input.addEventListener('change', update));

    function update() {
        const sex = document.getElementById('sex').value;
        const age = document.getElementById('age').value;
        const height_cm = document.getElementById('height').value;
        const weight_kg = document.getElementById('weight').value;
        const activity = document.getElementById('activity').value;
        const goal = document.getElementById('goal').value;

        fetch('/calculate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({sex, age, height_cm, weight_kg, activity, goal})
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById('tdee').textContent = `TDEE: ${data.tdee} kcal`;
            document.getElementById('calories').textContent = `Calories: ${data.tdee}`;
            document.getElementById('protein').textContent = `Protein: ${data.protein}g`;
            document.getElementById('fats').textContent = `Fats: ${data.fats}g`;
            document.getElementById('carbs').textContent = `Carbs: ${data.carbs}g`;
        });
    }
});