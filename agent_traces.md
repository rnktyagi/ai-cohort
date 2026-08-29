# LangChain Agent Test

## Setup

Used LangChain `create_agent` with the Day 13 tools:

- `check_coverage`
- `get_claim_status`
- `get_plan_details`

Model: `openai/gpt-oss-20b` via Groq

## Test Results

### Test 1
**Question:** Is physical therapy covered under plan SILVER?

**Result:** The agent called the coverage tool and returned that physical therapy is covered.

### Test 2
**Question:** What is the status of claim CLM001?

**Result:** The agent called the claim-status tool and returned **Approved**.

### Test 3
**Question:** What are the details of plan GOLD?

**Result:** The agent called the plan-details tool and returned **Gold PPO**, with a $2,000 deductible and 10% primary-care coinsurance after the deductible.

### Test 4
**Question:** Can you check whether dental surgery is covered under plan SILVER?

**Result:** The agent called the coverage tool and returned that dental surgery is covered.

### Test 5
**Question:** What is an insurance plan?

**Result:** The agent answered directly without needing a tool.

## Conclusion

All 5 test questions completed successfully. The agent selected the appropriate tools for coverage, claim, and plan questions and answered the general definition question directly.
