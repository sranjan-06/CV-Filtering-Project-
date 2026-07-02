from agents.validator_agent import CVValidatorAgent
from agents.privacy_agent import PrivacyAgent
from agents.summariser_agent import CVSummariserAgent
from agents.eligibility_agent import EligibilityCheckerAgent
from agents.ranking_agent import RankingAgent
from config import FAIRNESS_NOTICE


def run_cv_screening(employer_input):
    validator = CVValidatorAgent()
    privacy_agent = PrivacyAgent()
    summariser = CVSummariserAgent()
    eligibility_checker = EligibilityCheckerAgent()
    ranking_agent = RankingAgent()

    candidate_results = []
    warnings = []

    for candidate in employer_input["candidate_cvs"]:
        validation = validator.run({
            "job_description": employer_input["job_description"],
            "candidate": candidate,
            "priority_order": employer_input["priority_order"],
        })

        warnings.extend(validation.get("validation_warnings", []))
        warnings.extend(validation.get("priority_validation", {}).get("warnings", []))

        if not validation["is_valid"]:
            candidate_results.append({
                "candidate_id": candidate["candidate_id"],
                "validation": validation,
                "privacy": {},
                "summary": {
                    "summary_by_category": {},
                },
                "eligibility": {
                    "required_matches": [],
                    "preferred_matches": [],
                    "category_assessment": {},
                    "eligibility_status": "invalid_input",
                },
            })
            continue

        privacy = privacy_agent.run({
            "candidate_id": candidate["candidate_id"],
            "raw_text": candidate["raw_text"],
        })

        summary = summariser.run({
            "candidate_id": candidate["candidate_id"],
            "anonymous_profile_text": privacy["anonymous_profile_text"],
        })

        eligibility = eligibility_checker.run({
            "candidate_id": candidate["candidate_id"],
            "job_description": employer_input["job_description"],
            "category_weights": employer_input["category_weights"],
            "summary_by_category": summary["summary_by_category"],
        })

        candidate_results.append({
            "candidate_id": candidate["candidate_id"],
            "validation": validation,
            "privacy": {
                "candidate_id": privacy["candidate_id"],
                "privacy_actions": privacy["privacy_actions"],
            },
            "summary": summary,
            "eligibility": eligibility,
        })

    ranking = ranking_agent.run({
        "candidate_results": candidate_results,
        "category_weights": employer_input["category_weights"],
    })

    return {
        "priority_order": employer_input["priority_order"],
        "category_weights": employer_input["category_weights"],
        "shortlist": ranking["shortlist"],
        "selected_candidate_ids": ranking["selected_candidate_ids"],
        "warnings": list(set(warnings)),
        "fairness_notice": FAIRNESS_NOTICE,
    }