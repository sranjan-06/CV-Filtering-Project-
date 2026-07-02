from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process
from agents.base_agent import BaseAgent, get_llm
from config import VALID_CATEGORIES


class JobCriteria(BaseModel):
    required: list[str]
    preferred: list[str]


class EligibilityCheckerAgent(BaseAgent):
    def __init__(self):
        self.llm = get_llm()

        self.agent = Agent(
            role="Eligibility Checker Agent",
            goal=(
                "Extract required and preferred criteria from the job description, then compare "
                "candidate evidence against those criteria. Award credit only when evidence exists."
            ),
            backstory=(
                "You are an audit-focused recruitment analyst. You never award credit without "
                "evidence and every positive judgement must be traceable."
            ),
            llm=self.llm,
            verbose=False,
            allow_delegation=False,
        )

    def extract_job_criteria(self, job_description):
        task = Task(
            description=(
                "Extract required and preferred criteria from this job description.\n\n"
                f"{job_description}"
            ),
            expected_output=(
                "Return required and preferred as lists. Do not invent criteria."
            ),
            agent=self.agent,
            output_pydantic=JobCriteria,
        )

        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False,
        )

        try:
            output = crew.kickoff()
            return output.pydantic.model_dump()
        except Exception:
            return {
                "required": [],
                "preferred": [],
            }

    def find_match(self, requirement, summary_by_category):
        requirement_lower = requirement.lower()

        for category_data in summary_by_category.values():
            evidence_list = category_data.get("evidence", [])

            for evidence in evidence_list:
                if requirement_lower in evidence.lower():
                    return {
                        "status": "met",
                        "evidence": evidence,
                    }

        return {
            "status": "not_found",
            "evidence": "",
        }

    def assess_categories(self, summary_by_category, category_weights):
        assessment = {}

        for category in VALID_CATEGORIES:
            data = summary_by_category.get(category, {})
            evidence = data.get("evidence", [])

            assessment[category] = {
                "weighted_value": category_weights.get(category, 0),
                "status": "met" if evidence else "not_found",
                "evidence": evidence,
            }

        return assessment

    def run(self, payload):
        candidate_id = payload["candidate_id"]
        job_description = payload["job_description"]
        category_weights = payload["category_weights"]
        summary_by_category = payload["summary_by_category"]

        criteria = self.extract_job_criteria(job_description)

        required_matches = []
        preferred_matches = []

        for requirement in criteria["required"]:
            match = self.find_match(requirement, summary_by_category)
            required_matches.append({
                "requirement": requirement,
                "status": match["status"],
                "evidence": match["evidence"],
            })

        for requirement in criteria["preferred"]:
            match = self.find_match(requirement, summary_by_category)
            preferred_matches.append({
                "requirement": requirement,
                "status": match["status"],
                "evidence": match["evidence"],
            })

        met_required = sum(1 for item in required_matches if item["status"] == "met")
        total_required = max(len(required_matches), 1)

        ratio = met_required / total_required

        if ratio >= 0.8:
            status = "strong_match"
        elif ratio >= 0.5:
            status = "partial_match"
        else:
            status = "weak_match"

        return {
            "candidate_id": candidate_id,
            "required_matches": required_matches,
            "preferred_matches": preferred_matches,
            "category_assessment": self.assess_categories(summary_by_category, category_weights),
            "eligibility_status": status,
        }