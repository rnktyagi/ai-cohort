from langchain_core.tools import tool

@tool
def check_coverage(plan_id: str, procedure: str):
    """Check whether a procedure is covered under a specific insurance plan."""
    return {
        "plan_id": plan_id,
        "procedure": procedure,
        "covered": True,
        "details": f"{procedure} is covered under plan {plan_id}."
    }

@tool
def get_claim_status(claim_id: str):
    """Get the status of an insurance claim using its claim ID."""
    return {
        "claim_id": claim_id,
        "status": "Approved",
        "details": f"Claim {claim_id} has been approved."
    }

@tool
def get_plan_details(plan_id: str):
    """Get details about a specific insurance plan using its plan ID."""
    return {
        "plan_id": plan_id,
        "plan_name": "Gold PPO",
        "details": "Annual deductible: $2,000. Primary care: 10% coinsurance after deductible."
    }

tools = [
    check_coverage,
    get_claim_status,
    get_plan_details
]