document.addEventListener('DOMContentLoaded', () => {
    const genderInput = document.getElementById('gender');
    const ageInput = document.getElementById('age');
    const heightInput = document.getElementById('height');
    const weightInput = document.getElementById('weight');
    const activityInput = document.getElementById('activity');

    const tdeeOutput = document.getElementById('tdee-result');
    const caloriesOutput = document.getElementById('calories');
    const proteinOutput = document.getElementById('protein');
    const fatsOutput = document.getElementById('fats');
    const carbsOutput = document.getElementById('carbs');

    function calculateTDEE() {
        const gender = genderInput.value;
        const age = parseInt(ageInput.value);
        const height = parseInt(heightInput.value);
        const weight = parseInt(weightInput.value);
        const activity = parseFloat(activityInput.value);

        if (isNaN(age) || isNaN(height) || isNaN(weight) || isNaN(activity)) {
            tdeeOutput.textContent = 'Awaiting input...';
            caloriesOutput.textContent = '--';
            proteinOutput.textContent = '--g';
            fatsOutput.textContent = '--g';
            carbsOutput.textContent = '--g';
            return;
        }

        let bmr;
        if (gender === 'male') {
            bmr = 10 * weight + 6.25 * height - 5 * age + 5;
        } else {
            bmr = 10 * weight + 6.25 * height - 5 * age - 161;
        }

        const tdee = Math.round(bmr * activity);
        tdeeOutput.textContent = tdee;

        const protein = Math.round(weight * 2.2);
        const fats = Math.round((0.25 * tdee) / 9);
        const carbs = Math.round((tdee - (protein * 4 + fats * 9)) / 4);

        caloriesOutput.textContent = tdee;
        proteinOutput.textContent = `${protein}g`;
        fatsOutput.textContent = `${fats}g`;
        carbsOutput.textContent = `${carbs}g`;
    }

    [genderInput, ageInput, heightInput, weightInput, activityInput].forEach(input => {
        input.addEventListener('input', calculateTDEE);
    });

    calculateTDEE();
});