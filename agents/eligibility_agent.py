from agents.base_agent import BaseAgent
from config import VALID_CATEGORIES


class EligibilityCheckerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Eligibility Checker Agent")

    def run(self, payload):
        # TODO: Member 4 fills this in using Ollama and evidence matching
        return {
            "candidate_id": payload["candidate_id"],
            "required_matches": [],
            "preferred_matches": [],
            "category_assessment": {
                category: {
                    "weighted_value": payload["category_weights"].get(category, 0),
                    "status": "not_found",
                    "evidence": []
                }
                for category in VALID_CATEGORIES
            },
            "eligibility_status": "placeholder"
        }