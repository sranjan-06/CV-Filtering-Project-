from crewai import LLM
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_TEMPERATURE


def get_llm():
    return LLM(
        model=f"ollama/{OLLAMA_MODEL}",
        base_url=OLLAMA_BASE_URL,
        temperature=OLLAMA_TEMPERATURE,
    )


class BaseAgent:
    def run(self, payload: dict) -> dict:
        raise NotImplementedError("Agent must implement run().")