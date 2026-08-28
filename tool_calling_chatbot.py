from openai import OpenAI
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"]
)

class CoverageResult(BaseModel):
    plan_id: str
    procedure: str
    covered: bool
    details: str


class ClaimStatusResult(BaseModel):
    claim_id: str
    status: str
    details: str


class PlanDetailsResult(BaseModel):
    plan_id: str
    plan_name: str
    details: str


class OutOfPocketResult(BaseModel):
    procedure: str
    plan_id: str
    estimated_cost: float
    details: str

tools = [
    {
        "type": "function",
        "function": {
            "name": "check_coverage",
            "description": "Check whether a procedure is covered under a specific insurance plan.",
            "parameters": {
                "type": "object",
                "properties": {
                    "plan_id": {
                        "type": "string",
                        "description": "Insurance plan ID"
                    },
                    "procedure": {
                        "type": "string",
                        "description": "Medical procedure to check"
                    }
                },
                "required": ["plan_id", "procedure"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_claim_status",
            "description": "Get the status of an insurance claim.",
            "parameters": {
                "type": "object",
                "properties": {
                    "claim_id": {
                        "type": "string",
                        "description": "Insurance claim ID"
                    }
                },
                "required": ["claim_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_plan_details",
            "description": "Get details about an insurance plan.",
            "parameters": {
                "type": "object",
                "properties": {
                    "plan_id": {
                        "type": "string",
                        "description": "Insurance plan ID"
                    }
                },
                "required": ["plan_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "estimate_out_of_pocket_cost",
            "description": "Estimate the out-of-pocket cost for a procedure under an insurance plan.",
            "parameters": {
                "type": "object",
                "properties": {
                    "procedure": {
                        "type": "string",
                        "description": "Medical procedure"
                    },
                    "plan_id": {
                        "type": "string",
                        "description": "Insurance plan ID"
                    }
                },
                "required": ["procedure", "plan_id"]
            }
        }
    }
]

def check_coverage(plan_id, procedure):
    result = CoverageResult(
        plan_id=plan_id,
        procedure=procedure,
        covered=True,
        details=f"{procedure} is covered under plan {plan_id}."
    )

    return result.model_dump()


def get_claim_status(claim_id):
    result = ClaimStatusResult(
        claim_id=claim_id,
        status="Approved",
        details=f"Claim {claim_id} has been approved."
    )

    return result.model_dump()


def get_plan_details(plan_id):
    result = PlanDetailsResult(
        plan_id=plan_id,
        plan_name="Gold PPO",
        details="Annual deductible: $2,000. Primary care: 10% coinsurance after deductible."
    )

    return result.model_dump()


def estimate_out_of_pocket_cost(procedure, plan_id):
    result = OutOfPocketResult(
        procedure=procedure,
        plan_id=plan_id,
        estimated_cost=200.0,
        details=f"Estimated out-of-pocket cost for {procedure} under {plan_id}."
    )

    return result.model_dump()

tool_functions = {
    "check_coverage": check_coverage,
    "get_claim_status": get_claim_status,
    "get_plan_details": get_plan_details,
    "estimate_out_of_pocket_cost": estimate_out_of_pocket_cost
}

system_prompt = """
You are a helpful assistant that replies in a warm, respectful, and formal tone.

- Check the plan type and relevant section before answering.
- Use only confirmed information from the plan and cite the exact plan terms.
- Never infer or assume coverage.
- For medical advice or guidance, clearly state that you cannot provide medical advice and redirect the user to a licensed healthcare provider.
- Be empathetic when users discuss medical costs or distress.
"""

def run_agent(question):

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": question
        }
    ]

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if not message.tool_calls:
        return message.content

    messages.append(message)

    for tool_call in message.tool_calls:

        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        function = tool_functions[tool_name]

        result = function(**arguments)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })

    final_response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=tools,
        tool_choice="none"
    )

    return final_response.choices[0].message.content

test_questions = [
        "Is physical therapy covered under plan SILVER?",
        "What is the status of claim CLM001?",
        "What are the details of plan GOLD?",
        "How much would I pay out of pocket for an MRI under plan GOLD?",
        "Can you check whether dental surgery is covered under plan SILVER?",
        "What is an insurance plan?"
    ]

for i, question in enumerate(test_questions, 1):

    print(f"\n{'=' * 60}")
    print(f"Test {i}")
    print(f"Question: {question}")

    answer = run_agent(question)

    print(f"Answer: {answer}")