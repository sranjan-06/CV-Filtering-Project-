from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/screen", methods=["POST"])
def screen():
    return jsonify({
        "fairness_notice": "This system supports employer review but does not make final hiring decisions.",
        "category_weights": {
            "Experience": 30,
            "Skills": 25,
            "Projects": 20,
            "Education": 15,
            "Extracurriculars": 10
        },
        "warnings": [],
        "shortlist": [
            {
                "rank": 1,
                "candidate_id": "CAND-001",
                "score": 86,
                "confidence": "High",
                "reason": "Strong required match and strong evidence in the employer's highest-valued categories.",
                "missing_requirements": ["Docker"],
                "human_review_note": "Employer should verify Docker or deployment experience before making a final decision."
            }
        ]
    })


if __name__ == "__main__":
    app.run(debug=True)