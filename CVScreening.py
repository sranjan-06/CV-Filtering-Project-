# placeholder python file
# help

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
    goal="Check CV to ensure it is formatted correctly and send it to the privacy agent. The correct format is a text file.",
    backstory="You are an experienced software engineer who is checking to ensure that all CVs are of the right file type.",
    llm=llm,
)

agent_two = Agent(
    role="Privacy",
    goal="",
    backstory="...",
    llm=llm,
)

agent_three = Agent(
    role="CVSummary",
    goal="...",
    backstory="...",
    llm=llm,
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


