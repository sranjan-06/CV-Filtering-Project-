# Employer-Facing Agentic CV Screener

This project is an employer-facing agentic CV screening support tool.

It is designed for employers, recruiters, hiring managers, internship coordinators, and admissions reviewers.

It is not designed for candidates.

## Pipeline

1. Employer uploads job description and candidate CVs
2. Employer ranks five categories
3. CV Validator Agent checks input
4. Privacy Agent anonymises CVs
5. CV Summariser Agent creates structured summaries
6. Eligibility Checker Agent checks job match
7. Ranking Agent creates anonymous shortlist

## Important Notice

This system supports employer review but does not make final hiring decisions.

## Local Setup

```bash
pip install -r requirements.txt
python app.py