import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "granite4.1:3b")
OLLAMA_TEMPERATURE = 0.3

VALID_CATEGORIES = [
    "Education",
    "Extracurriculars",
    "Projects",
    "Experience",
    "Skills",
]

CATEGORY_WEIGHTS_BY_RANK = [30, 25, 20, 15, 10]

FAIRNESS_NOTICE = (
    "This system supports employer review but does not make final hiring decisions."
)