from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process
from agents.base_agent import BaseAgent, get_llm


class PrivacyResult(BaseModel):
    anonymous_profile_text: str
    contact_information: str
    privacy_actions: list[str]


class PrivacyAgent(BaseAgent):
    def __init__(self):
        self.llm = get_llm()

        self.agent = Agent(
            role="Privacy Agent",
            goal=(
                "Remove personal and demographic information from a CV before scoring. "
                "Replace personal details with clear placeholders such as [EMAIL REMOVED], "
                "[PHONE REMOVED], [NAME REMOVED], or [PII REMOVED]. "
                "Preserve job-related skills, projects, education, experience, and extracurricular evidence."
            ),
            backstory=(
                "You are a compliance specialist focused on fair recruitment. "
                "You remove information that could create bias while preserving evidence needed for job matching."
            ),
            llm=self.llm,
            verbose=False,
            allow_delegation=False,
        )

    def run(self, payload):
        candidate_id = payload["candidate_id"]
        raw_text = payload["raw_text"]

        task = Task(
            description=(
                "Anonymise this CV. Remove names, emails, phone numbers, addresses, "
                "postcodes, LinkedIn, GitHub, personal websites, age, gender, nationality, "
                "religion, marital status, and other demographic identifiers.\n\n"
                f"{raw_text}"
            ),
            expected_output=(
                "Return anonymous_profile_text, contact_information, and privacy_actions. "
                "Do not summarise. Do not remove job-related evidence."
            ),
            agent=self.agent,
            output_pydantic=PrivacyResult,
        )

        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False,
        )

        try:
            output = crew.kickoff()
            result = output.pydantic

            return {
                "candidate_id": candidate_id,
                "anonymous_profile_text": result.anonymous_profile_text,
                "contact_information": result.contact_information,
                "privacy_actions": result.privacy_actions,
            }

        except Exception as error:
            return {
                "candidate_id": candidate_id,
                "anonymous_profile_text": raw_text,
                "contact_information": "",
                "privacy_actions": [f"Privacy agent failed: {error}"],
            }