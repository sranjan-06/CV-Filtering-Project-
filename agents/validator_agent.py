from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process
from agents.base_agent import BaseAgent, get_llm
from config import VALID_CATEGORIES


class FormatCheckResult(BaseModel):
    valid_format: bool
    reason_invalid: str = ""


class CVValidatorAgent(BaseAgent):
    def __init__(self):
        self.llm = get_llm()

        self.agent = Agent(
            role="CV Validator",
            goal=(
                "Check whether the uploaded document is a usable CV. "
                "Default to accepting the document. Only reject if it is blank, unreadable, "
                "corrupted, or clearly not a CV. Do not judge candidate quality."
            ),
            backstory=(
                "You are a careful CV validation specialist. You understand that real CVs "
                "can be short, messy, unconventional, or missing standard headings. "
                "You only reject documents that are genuinely unusable."
            ),
            llm=self.llm,
            verbose=False,
            allow_delegation=False,
        )

    def validate_priority_order(self, priority_order):
        warnings = []

        if len(priority_order) != 5:
            warnings.append("Employer must rank all five categories.")

        duplicates = [
            category for category in set(priority_order)
            if priority_order.count(category) > 1
        ]

        missing = [
            category for category in VALID_CATEGORIES
            if category not in priority_order
        ]

        invalid = [
            category for category in priority_order
            if category not in VALID_CATEGORIES
        ]

        if duplicates:
            warnings.append(f"Duplicate priority categories found: {duplicates}")

        if missing:
            warnings.append(f"Missing priority categories: {missing}")

        if invalid:
            warnings.append(f"Invalid priority categories found: {invalid}")

        return {
            "is_valid": len(warnings) == 0,
            "warnings": warnings,
        }

    def run(self, payload):
        candidate = payload["candidate"]
        raw_text = candidate.get("raw_text", "")
        filename = candidate.get("filename", "")
        priority_order = payload["priority_order"]
        job_description = payload["job_description"]

        warnings = []

        if not job_description or not job_description.strip():
            warnings.append("Job description is empty.")

        if not filename.endswith(".txt"):
            warnings.append("Unsupported file type. Only .txt CV files are accepted.")

        if not raw_text or not raw_text.strip():
            warnings.append("CV is empty or whitespace-only.")

        priority_validation = self.validate_priority_order(priority_order)

        if warnings:
            return {
                "candidate_id": candidate["candidate_id"],
                "is_valid": False,
                "validation_warnings": warnings,
                "priority_validation": priority_validation,
            }

        task = Task(
            description=(
                "Here is the raw text extracted from an uploaded document:\n\n"
                f"{raw_text}\n\n"
                "Decide whether this is a valid, usable CV."
            ),
            expected_output=(
                "Return structured output with valid_format true or false and reason_invalid."
            ),
            agent=self.agent,
            output_pydantic=FormatCheckResult,
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

            if not result.valid_format:
                warnings.append(result.reason_invalid)

            return {
                "candidate_id": candidate["candidate_id"],
                "is_valid": result.valid_format and priority_validation["is_valid"],
                "validation_warnings": warnings,
                "priority_validation": priority_validation,
            }

        except Exception as error:
            return {
                "candidate_id": candidate["candidate_id"],
                "is_valid": False,
                "validation_warnings": [f"Validator failed: {error}"],
                "priority_validation": priority_validation,
            }