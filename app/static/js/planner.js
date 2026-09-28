async function generatePlan(plannerType, formData) {
    const resultBox = document.getElementById("result");

    if (!resultBox) {
        console.error("Result box not found.");
        return;
    }

    resultBox.innerHTML = "Generating your smart plan...";

    try {
        const response = await fetch(`/api/planners/${plannerType}`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        console.log("Planner response:", data);

        if (!response.ok) {
            const errorMessage =
                typeof data.detail === "string"
                    ? data.detail
                    : JSON.stringify(data.detail || data);

            resultBox.innerHTML =
                `<div class="error-message">Could not generate recommendation: ${errorMessage}</div>`;
            return;
        }

        // Get the recommendation safely
        let recommendation = data.recommendation;

        if (recommendation === undefined || recommendation === null) {
            recommendation = data.message;
        }

        // If Gemini/backend returned an object, convert it properly
        if (typeof recommendation === "object") {
            recommendation = JSON.stringify(
                recommendation,
                null,
                2
            );
        }

        if (!recommendation) {
            recommendation = "No recommendation was generated.";
        }

        resultBox.innerHTML = `
            <div class="recommendation-box">
                <h3>✨ Your Smart Plan</h3>
                <pre>${escapeHtml(String(recommendation))}</pre>
            </div>
        `;

    } catch (error) {
        console.error("Planner error:", error);

        resultBox.innerHTML = `
            <div class="error-message">
                Could not generate recommendation. Please try again.
            </div>
        `;
    }
}


function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}