from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process
from agents.base_agent import BaseAgent, get_llm
from config import VALID_CATEGORIES


class CategorySummary(BaseModel):
    summary: str
    evidence: list[str]
    confidence: str


class CVSummary(BaseModel):
    Education: CategorySummary
    Extracurriculars: CategorySummary
    Projects: CategorySummary
    Experience: CategorySummary
    Skills: CategorySummary


class CVSummariserAgent(BaseAgent):
    def __init__(self):
        self.llm = get_llm()

        self.agent = Agent(
            role="CV Summariser Agent",
            goal=(
                "Convert an anonymised CV into a structured five-category summary: "
                "Education, Extracurriculars, Projects, Experience, and Skills. "
                "Use only evidence from the CV. Do not invent claims."
            ),
            backstory=(
                "You are a CV evidence specialist. You structure messy CV text into clear, "
                "auditable evidence that hiring reviewers can inspect."
            ),
            llm=self.llm,
            verbose=False,
            allow_delegation=False,
        )

    def fallback_summary(self):
        return {
            category: {
                "summary": "No clear evidence found.",
                "evidence": [],
                "confidence": "Low",
            }
            for category in VALID_CATEGORIES
        }

    def run(self, payload):
        candidate_id = payload["candidate_id"]
        anonymous_text = payload["anonymous_profile_text"]

        task = Task(
            description=(
                "Summarise this anonymised CV into exactly five categories:\n"
                "Education, Extracurriculars, Projects, Experience, Skills.\n\n"
                "For each category, provide summary, evidence snippets, and confidence "
                "as High, Medium, or Low.\n\n"
                f"{anonymous_text}"
            ),
            expected_output=(
                "Strict structured output with all five categories. "
                "Do not invent unsupported claims."
            ),
            agent=self.agent,
            output_pydantic=CVSummary,
        )

        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False,
        )

        try:
            output = crew.kickoff()
            result = output.pydantic.model_dump()

            return {
                "candidate_id": candidate_id,
                "summary_by_category": result,
            }

        except Exception:
            return {
                "candidate_id": candidate_id,
                "summary_by_category": self.fallback_summary(),
            }