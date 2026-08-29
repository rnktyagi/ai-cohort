from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LITELLM_DROP_PARAMS"] = "true"

@tool("check_coverage")
def check_coverage(plan_id: str, procedure: str):
    """Check whether a procedure is covered under an insurance plan."""
    return {
        "plan_id": plan_id,
        "procedure": procedure,
        "covered": True,
        "details": f"{procedure} is covered under plan {plan_id}."
    }

@tool("get_claim_status")
def get_claim_status(claim_id: str):
    """Get the status of an insurance claim."""
    return {
        "claim_id": claim_id,
        "status": "Approved",
        "details": f"Claim {claim_id} has been approved."
    }

load_dotenv()

llm = LLM(
    model="groq/openai/gpt-oss-20b",
    api_key=os.environ["GROQ_API_KEY"],
    temperature=0
)

coverage_specialist = Agent(
    role="Coverage Specialist",
    goal="Answer insurance coverage questions using retrieval and coverage tools.",
    backstory="You specialize in insurance coverage, benefits, deductibles, copays, and covered procedures.",
    llm=llm,
    tools=[check_coverage],
    verbose=True
)

claims_specialist = Agent(
    role="Claims Specialist",
    goal="Answer insurance claim questions using retrieval and claim tools.",
    backstory="You specialize in claim status and claim-related questions.",
    llm=llm,
    tools=[get_claim_status],
    verbose=True
)

router = Agent(
    role="Router",
    goal="Classify each user question as coverage, claims, or enrollment and choose the correct specialist.",
    backstory="You route insurance questions to the specialist best suited to answer them.",
    llm=llm,
    verbose=True
)

router_task = Task(
    description="Classify the user's question as coverage, claims, or enrollment and identify the correct specialist.",
    expected_output="Return exactly one category: coverage, claims, or enrollment.",
    agent=router
)

coverage_task = Task(
    description="Answer coverage questions using the available coverage retrieval and tools. Do not guess coverage.",
    expected_output="A clear, accurate answer based only on confirmed coverage information.",
    agent=coverage_specialist
)

claims_task = Task(
    description="Answer claims questions using the available claim retrieval and tools. Do not guess claim information.",
    expected_output="A clear, accurate answer based only on confirmed claim information.",
    agent=claims_specialist
)

crew = Crew(
    agents=[
        router,
        coverage_specialist,
        claims_specialist
    ],
    process=Process.sequential,
    verbose=True
)

def run_crew(question):
    router_result = router.kickoff(
        f"Classify this question as exactly one of: coverage, claims, enrollment.\n\nQuestion: {question}"
    )

    category = router_result.raw.strip().lower()

    if "coverage" in category:
        result = coverage_specialist.kickoff(
            f"Answer this question using the available coverage tools. Do not guess coverage.\n\nQuestion: {question}"
        )
    elif "claims" in category:
        result = claims_specialist.kickoff(
            f"Answer this question using the available claim tools. Do not guess claim information.\n\nQuestion: {question}"
        )
    else:
        result = "Enrollment questions are not handled by the current specialists."

    return result.raw if hasattr(result, "raw") else result

test_questions = [
    "Is physical therapy covered under plan SILVER?",
    "What is the status of claim CLM001?",
    "What are the details of plan GOLD?",
    "Can you check whether dental surgery is covered under plan SILVER?",
    "What is an insurance plan?"
]

for i, question in enumerate(test_questions, 1):
    print(f"\n{'=' * 60}")
    print(f"Test {i}")
    print(f"Question: {question}")

    answer = run_crew(question)

    print("Answer:")
    print(answer)