from agents.base_agent import BaseAgent


class RankingAgent(BaseAgent):
    def __init__(self):
        super().__init__("Ranking Agent")

    def run(self, payload):
        # TODO: Member 5 fills this in with real scoring
        shortlist = []

        for index, result in enumerate(payload["candidate_results"], start=1):
            shortlist.append({
                "rank": index,
                "candidate_id": result["candidate_id"],
                "score": 0,
                "confidence": "Low",
                "category_weights": payload["category_weights"],
                "reason": "Placeholder ranking. Ranking Agent not implemented yet.",
                "missing_requirements": [],
                "human_review_note": "Human employer must review before making any final decision."
            })

        return {
            "shortlist": shortlist,
            "selected_candidate_ids": [item["candidate_id"] for item in shortlist]
        }