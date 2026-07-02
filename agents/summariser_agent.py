from agents.base_agent import BaseAgent
from config import VALID_CATEGORIES


class CVSummariserAgent(BaseAgent):
    def __init__(self):
        super().__init__("CV Summariser Agent")

    def run(self, payload):
        # TODO: Member 3 fills this in using Ollama
        return {
            "candidate_id": payload["candidate_id"],
            "summary_by_category": {
                category: {
                    "summary": "Placeholder summary. Agent not implemented yet.",
                    "evidence": [],
                    "confidence": "Low"
                }
                for category in VALID_CATEGORIES
            }
        }