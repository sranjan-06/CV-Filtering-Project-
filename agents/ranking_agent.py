from agents.base_agent import BaseAgent
from services.scoring import calculate_score


class RankingAgent(BaseAgent):
    def confidence_from_score(self, score):
        if score >= 75:
            return "High"
        if score >= 50:
            return "Medium"
        return "Low"

    def get_missing_requirements(self, required_matches):
        return [
            item["requirement"]
            for item in required_matches
            if item["status"] != "met"
        ]

    def build_reason(self, score):
        if score >= 75:
            return "Strong match with clear evidence in employer-prioritised areas."
        if score >= 50:
            return "Partial match with some evidence, but requires human review."
        return "Limited evidence against the job description and employer priorities."

    def run(self, payload):
        shortlist = []

        for result in payload["candidate_results"]:
            candidate_id = result["candidate_id"]
            summary = result["summary"]
            eligibility = result["eligibility"]

            score = calculate_score(
                eligibility["required_matches"],
                eligibility["preferred_matches"],
                eligibility["category_assessment"],
                summary["summary_by_category"],
            )

            missing = self.get_missing_requirements(eligibility["required_matches"])

            shortlist.append({
                "rank": None,
                "candidate_id": candidate_id,
                "score": score,
                "confidence": self.confidence_from_score(score),
                "category_weights": payload["category_weights"],
                "reason": self.build_reason(score),
                "missing_requirements": missing,
                "human_review_note": (
                    "Employer should review the evidence and missing requirements before making any final decision."
                ),
            })

        shortlist.sort(key=lambda item: (-item["score"], item["candidate_id"]))

        for index, candidate in enumerate(shortlist, start=1):
            candidate["rank"] = index

        return {
            "shortlist": shortlist,
            "selected_candidate_ids": [
                candidate["candidate_id"] for candidate in shortlist
            ],
        }