const form = document.getElementById("screenForm");
const loading = document.getElementById("loading");
const results = document.getElementById("results");
const errorBox = document.getElementById("error");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    clearMessages();
    showLoading(true);

    const formData = new FormData(form);

    try {
        const response = await fetch("/screen", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong while screening CVs.");
        }

        renderResults(data);

    } catch (error) {
        showError(error.message);
    } finally {
        showLoading(false);
    }
});

function clearMessages() {
    results.innerHTML = "";
    errorBox.textContent = "";
    errorBox.style.display = "none";
}

function showLoading(isLoading) {
    if (isLoading) {
        loading.classList.remove("hidden");
    } else {
        loading.classList.add("hidden");
    }
}

function showError(message) {
    errorBox.textContent = message;
    errorBox.style.display = "block";
}

function renderResults(data) {
    let html = `
        <h2>Anonymous Shortlist Results</h2>
        <p class="notice">${escapeHtml(data.fairness_notice || "This system supports employer review but does not make final hiring decisions.")}</p>
    `;

    if (data.category_weights) {
        html += `
            <div class="weights-box">
                <h3>Category Weights Used</h3>
                <pre>${escapeHtml(JSON.stringify(data.category_weights, null, 2))}</pre>
            </div>
        `;
    }

    if (data.warnings && data.warnings.length > 0) {
        html += `
            <div class="warnings-box">
                <h3>Warnings</h3>
                <ul>
                    ${data.warnings.map(warning => `<li>${escapeHtml(warning)}</li>`).join("")}
                </ul>
            </div>
        `;
    }

    if (!data.shortlist || data.shortlist.length === 0) {
        html += `<p>No candidates were ranked. Please check the uploaded files and try again.</p>`;
        results.innerHTML = html;
        return;
    }

    data.shortlist.forEach(candidate => {
        const confidenceClass = getConfidenceClass(candidate.confidence);

        html += `
            <div class="result-card">
                <h3>Rank ${escapeHtml(candidate.rank)} — ${escapeHtml(candidate.candidate_id)}</h3>

                <p class="score">Score: ${escapeHtml(candidate.score)} / 100</p>

                <p>
                    <strong>Confidence:</strong>
                    <span class="${confidenceClass}">
                        ${escapeHtml(candidate.confidence)}
                    </span>
                </p>

                <p><strong>Reason:</strong> ${escapeHtml(candidate.reason)}</p>

                <p>
                    <strong>Missing Requirements:</strong>
                    ${
                        candidate.missing_requirements && candidate.missing_requirements.length > 0
                            ? escapeHtml(candidate.missing_requirements.join(", "))
                            : "None clearly identified"
                    }
                </p>

                <p>
                    <strong>Human Review Note:</strong>
                    ${escapeHtml(candidate.human_review_note)}
                </p>
            </div>
        `;
    });

    results.innerHTML = html;
}

function getConfidenceClass(confidence) {
    if (!confidence) return "confidence-low";

    const value = confidence.toLowerCase();

    if (value === "high") return "confidence-high";
    if (value === "medium") return "confidence-medium";

    return "confidence-low";
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}