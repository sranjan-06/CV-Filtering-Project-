from flask import Flask, render_template, request, jsonify

from orchestrator.crew_orchestrator import run_cv_screening
from services.priority_weights import convert_priority_order_to_weights


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/screen", methods=["POST"])
def screen():
    try:
        job_description = request.form.get("job_description", "").strip()
        priority_order = request.form.getlist("priority_order[]")
        uploaded_files = request.files.getlist("candidate_cvs")

        if not uploaded_files:
            return jsonify({
                "error": "Please upload at least one candidate CV."
            }), 400

        candidate_cvs = []

        for index, uploaded_file in enumerate(uploaded_files, start=1):
            raw_text = uploaded_file.read().decode("utf-8", errors="ignore")

            candidate_cvs.append({
                "candidate_id": f"CAND-{index:03d}",
                "filename": uploaded_file.filename,
                "raw_text": raw_text
            })

        category_weights = convert_priority_order_to_weights(priority_order)

        employer_input = {
            "job_description": job_description,
            "candidate_cvs": candidate_cvs,
            "priority_order": priority_order,
            "category_weights": category_weights
        }

        result = run_cv_screening(employer_input)

        return jsonify(result)

    except Exception as error:
        return jsonify({
            "error": str(error),
            "fairness_notice": "This system supports employer review but does not make final hiring decisions."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)