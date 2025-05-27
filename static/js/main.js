
document.addEventListener("DOMContentLoaded", () => {
    const gender = document.getElementById("gender");
    const age = document.getElementById("age");
    const height = document.getElementById("height");
    const weight = document.getElementById("weight");
    const activity = document.getElementById("activity");
    const tdeeValue = document.getElementById("tdee-value");

    const recalculate = () => {
        const heightVal = height.value.split("|")[1].trim().split(" ")[0];
        const weightVal = weight.value.split("|")[1].trim().split(" ")[0];

        fetch("/tdee", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                gender: gender.value,
                age: age.value,
                height_cm: heightVal,
                weight_kg: weightVal,
                activity_level: activity.value,
            }),
        })
        .then(res => res.json())
        .then(data => {
            tdeeValue.textContent = data.tdee + " kcal/day";
        });
    };

    [gender, age, height, weight, activity].forEach(el => el.addEventListener("change", recalculate));
});
