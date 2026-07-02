from agents.base_agent import BaseAgent


class PrivacyAgent(BaseAgent):
    def __init__(self):
        super().__init__("Privacy Agent")

    def run(self, payload):
        # TODO: Member 2 fills this in
        return {
            "candidate_id": payload["candidate_id"],
            "anonymous_profile_text": payload["raw_text"],
            "privacy_actions": []
        }