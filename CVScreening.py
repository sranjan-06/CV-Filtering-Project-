# placeholder python file
# help 
#hello it is sury 

# new comment

from crewai import Agent, Task, Crew, Process, LLM

VERBOSE = False
TRACING = True

# Model Initialisation
llm = LLM(
    model="ollama/granite4.1:3b",
    base_url="http://localhost:11434",
    temperature=0.3,
)

# ======================================================================
# STEP 1 — DESIGNING YOUR AGENTS
# ======================================================================

agent_one = Agent(
    role="CVFormatting",
    goal="Check CV to ensure it is formatted correctly and send it to the privacy agent. The correct format is a text file. You will also ensure the presence of at least some recognizable CV sections or content, such as work experience, education, or skills (they don't need to be formally labeled, but the substance should be identifiable).  That there is enough content to meaningfully evaluate (not just a name and one line of text). Do not evaluate the quality, relevance, or strength of the candidate's experience — only whether the document is structurally valid and usable by other agents. Do not make any changes to the document. Do not edit or summarise.",
    backstory="You are an experienced software engineer who is checking to ensure that all CVs are of the right file type. You're the first checkpoint in the pipeline, and you take that seriously. Before anyone else touches a document, you check that it's actually a CV - not a cover letter, a corrupted file, a blank page, or something uploaded by mistake. You verify the text extracted cleanly, that key sections like experience, education, or skills are present in some recognizable form, and that the content is coherent enough to work with. If something looks off - garbled text, missing structure, wrong document type - you flag it immediately rather than letting a broken file waste everyone else's time downstream. You're not here to judge quality or content, only to confirm the document is what it claims to be and usable.",
    llm=llm,
)

agent_two = Agent(
    role="PrivacyProtector",
    goal="You will receive a CV from the CVFormatting agent. You will need to remove all personally identifiable information from the CV and instead replace it with PII. You will also assign a unique applicant ID for each applicant. This application ID will be a two digit number that is unique to each applicant. Store each applicant's personal information seperately, where it is tagged to their application ID (in a seperate document titled 'Contact Information'. Then, send the CV without any personally identifiable information to the next agent. Personal information would include: Name, Age, Gender, Address, Email Address, Home Address, Phone Number, Date of Birth, Nationality, Religion, Marital Status, Sexual Orientation, Any other demographic identifier, Any photos. Try to preserve the original formatting and structure as much as possible only substitute the information with PII. Do not make any other changes. Do not summarise. Ensure all personal information has been moved to the applicant ID document.",
    backstory="You are a compliance specialist who's seen how bias creeps into hiring the moment a name, photo, or address enters the picture. You believe candidates should be judged on skills alone, so you strip every CV of anything that could identify or bias evaluation: names, contact details, photos, addresses, ages, nationality, and personal social links. You're precise and conservative, when in doubt, you redact. But you never touch what matters: job titles, employers, education, skills, and dates. Your work is what makes fair, skills-based screening possible. You also ensure that all information is stored safely elsewhere for human auditors to cross-check later",
    llm=llm,
)

agent_three = Agent(
    role="Senior CV Sentence Classification Specialist",

    goal=(
        "Read the full text of a single candidate CV and classify every "
        "substantive sentence or bullet point into exactly one of five "
        "categories — Education, Extra Curriculars, Projects, Experiences, "
        "or Skills — preserving the candidate's original wording, without "
        "summarizing, judging, scoring, or inventing content, and return "
        "the result as strict JSON with all five categories present as keys."
    ),

    backstory=(
        "You spent 8 years as a technical recruiter and resume-screening "
        "consultant for Fortune 500 hiring teams, personally structuring "
        "over 20,000 CVs across engineering, product, and design roles. "
        "You are known for obsessive literal accuracy — you never "
        "paraphrase a candidate's own words, and you have a sharp instinct "
        "for telling a paid internship apart from a personal side project "
        "apart from a university club activity, even when the phrasing is "
        "ambiguous. You built your reputation by turning messy, "
        "inconsistently formatted resumes into perfectly organized category "
        "breakdowns that hiring managers could scan in seconds. You never "
        "drop a relevant line, and you never invent one that isn't in the "
        "source text."
    ),

    llm=llm,
    verbose=True,          # optional: prints the agent's reasoning steps
    allow_delegation=False # optional: this agent shouldn't hand work to others
)
agent_four = Agent(
    role="EligibilityChecker",
    goal="...",
    backstory="...",
    llm=llm,
)
agent_five = Agent(
    role="Ranking",
    goal="...",
    backstory="...",
    llm=llm,
)

# ======================================================================
# STEP 2 — PUT YOUR AGENTS ON THE TEAM
# ----------------------------------------------------------------------
# List every agent you created so the manager knows who's available.
# ======================================================================

my_team = [
    agent_one,
    agent_two,
    agent_three,
    agent_four,
    agent_five,
]


# ======================================================================
# STEP 3 — HANDLE A REQUEST  (you usually DON'T need to change this)
# ----------------------------------------------------------------------
# The manager reads the request + history and delegates to the right agent.
# Notice the Task has NO `agent=` — that's on purpose. The manager picks.
# ======================================================================

conversation = []   # remembers what's been said so far

def handle(user_request):
    history = "\n".join(conversation)
    task = Task(
        description=(
            f"Conversation so far:\n{history if history else '(nothing yet)'}\n\n"
            f"The user now says: '{user_request}'. Fulfil their request, "
            "using the earlier conversation for context."
        ),
        expected_output="A clear, helpful answer for the user.",
    )
    crew = Crew(
        agents=my_team,
        tasks=[task],
        process=Process.hierarchical,   # the manager/orchestrator
        manager_llm=llm,
        verbose=VERBOSE,
        tracing=TRACING,
    )
    result = crew.kickoff()

    conversation.append(f"User: {user_request}")
    conversation.append(f"Assistant: {result}")
    return result


# ======================================================================
# STEP 4 — CHAT LOOP  (customise the welcome text for your team!)
# ======================================================================

if __name__ == "__main__":
    # TODO: change these lines to describe YOUR team and give example prompts
    print("My Agent Team is ready! Try things like:")
    print(" - I want to learn basic algebra. Quiz me.")
    print(" - Ask me questions about book binding.")
    print("(type 'quit' to exit)\n")

    while True:
        request = input("What to do you want to learn? ").strip()
        if request.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break
        if not request:
            continue

        result = handle(request)
        print("\nFinal answer:\n" + str(result) + "\n")


