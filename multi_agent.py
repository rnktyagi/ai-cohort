from crewai import Agent, Task, Crew, Process, LLM
import os
from dotenv import load_dotenv
from memory.memory import get_history, save_message

load_dotenv()

from crewai.tools import tool
import asyncio
from tools.mcp_client import call_mcp_tool

@tool("check_coverage")
def check_coverage_mcp(plan_id: str, procedure: str):
    """Check coverage through the MCP server."""
    for attempt in range(2):
        try:
            return asyncio.run(
                asyncio.wait_for(
                    call_mcp_tool(
                        "check_coverage",
                        {
                            "plan_id": plan_id,
                            "procedure": procedure
                        }
                    ),
                    timeout=10
                )
            )
        except Exception:
            if attempt == 1:
                return "I'm having trouble accessing that right now, please contact member support"


@tool("get_claim_status")
def get_claim_status_mcp(claim_id: str):
    """Get claim status through the MCP server."""
    for attempt in range(2):
        try:
            return asyncio.run(
                asyncio.wait_for(
                    call_mcp_tool(
                        "get_claim_status",
                        {
                            "claim_id": claim_id
                        }
                    ),
                    timeout=10
                )
            )
        except Exception:
            if attempt == 1:
                return "I'm having trouble accessing that right now, please contact member support"

llm = LLM(
    model="groq/openai/gpt-oss-20b",
    api_key=os.environ["GROQ_API_KEY"],
    temperature=0
)

coverage_specialist = Agent(
    role="Coverage Specialist",
    goal="Answer insurance coverage questions using the MCP coverage tool.",
    backstory="You specialize in insurance coverage, benefits, deductibles, copays, and covered procedures.",
    llm=llm,
    tools=[check_coverage_mcp],
    verbose=True
)

claims_specialist = Agent(
    role="Claims Specialist",
    goal="Answer insurance claim questions using the MCP claim tool.",
    backstory="You specialize in claim status and claim-related questions.",
    llm=llm,
    tools=[get_claim_status_mcp],
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