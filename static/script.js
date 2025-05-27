
function getSelectedValue(id) {
    return document.getElementById(id).value;
}

function getNumericValue(selectId) {
    let val = getSelectedValue(selectId).split("|")[1];
    return parseFloat(val.trim().replace(/[^0-9.]/g, ""));
}

function recalculate() {
    const gender = getSelectedValue("gender");
    const age = parseInt(getSelectedValue("age"));
    const height = getNumericValue("height");
    const weight = getNumericValue("weight");
    const activity = getSelectedValue("activity");
    const goal = getSelectedValue("goal");

    console.log("Calculating with:", { gender, age, height, weight, activity, goal });

    fetch("/tdee", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ gender, age, height, weight, activity })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("tdee-output").innerHTML = `
            <strong>Your TDEE is ${data.tdee} calories/day.</strong><br>
            Your BMR is ${data.bmr} calories/day — this is the energy needed at complete rest.<br>
            Your activity level ('${data.activity_label}') increases your daily burn by ${data.multiplier}×.<br>
            To cut: ${data.cut} kcal/day. To bulk: ${data.bulk} kcal/day.
        `;

        fetch("/macros", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ tdee: data.tdee, goal, weight, gender })
        })
        .then(res => res.json())
        .then(macros => {
            document.getElementById("macro-output").innerHTML = `
                Calories: ${macros.calories}<br>
                Protein: ${macros.protein} g<br>
                Fats: ${macros.fats} g<br>
                Carbs: ${macros.carbs} g
            `;
        });
    });
}

function populateDropdown(id, values) {
    const dropdown = document.getElementById(id);
    dropdown.innerHTML = values.map(v => `<option value="${v}">${v}</option>`).join("");
}

document.addEventListener("DOMContentLoaded", () => {
    const ages = Array.from({length: 108}, (_, i) => `${i + 13} yrs`);
    const heights = Array.from({length: 32}, (_, i) => {
        const ft = Math.floor(i / 12) + 4;
        const inch = i % 12;
        const totalInches = ft * 12 + inch;
        const cm = (totalInches * 2.54).toFixed(2);
        return `${ft}'${inch}" | ${cm} cm`;
    });
    const weights = Array.from({length: 641}, (_, i) => {
        const lbs = i + 60;
        const kg = (lbs * 0.453592).toFixed(2);
        return `${lbs} lbs | ${kg} kg`;
    });

    populateDropdown("age", ages);
    populateDropdown("height", heights);
    populateDropdown("weight", weights);

    ["gender", "age", "height", "weight", "activity", "goal"].forEach(id => {
        document.getElementById(id).addEventListener("change", recalculate);
    });

    recalculate();  // initial load
});
