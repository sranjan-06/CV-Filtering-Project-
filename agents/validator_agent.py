from agents.base_agent import BaseAgent


class CVValidatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("CV Validator Agent")

    def run(self, payload):
        # TODO: Member 1 fills this in
        return {
            "candidate_id": payload["candidate"]["candidate_id"],
            "is_valid": True,
            "validation_warnings": [],
            "priority_validation": {
                "is_valid": True,
                "warnings": []
            }
        }