# GOVERNANCE.md

## 1. Data Sources and Sensitivity

This chatbot uses the project's insurance data sources:

- **`plans.csv`** — contains insurance plan information. This is sensitive insurance/business data because it describes member plan coverage and benefits.
- **`claims.csv`** — contains claim information and is more sensitive because claims can relate to an individual's healthcare activity.

The chatbot also uses retrieved policy content and conversation history when answering questions.

## 2. PHI / PII Fields

The project may handle fields related to:

- **member_id** — identifies a member and should be treated as sensitive personal information.
- **claim details** — may reveal information about a member's healthcare-related activity and should be handled as sensitive.
- **procedures** — may describe healthcare services associated with a member or claim and should be treated as sensitive.

Access to these fields should be limited to what is required to answer the user's question.

## 3. Bias and Fairness Risks

A key risk is making assumptions based on **plan tier**. For example, the chatbot should not assume that a Gold plan automatically provides better coverage for every procedure than Silver or Bronze plans.

Other risks include:

- Assuming coverage when the source does not explicitly confirm it.
- Giving different answers because information is missing for one plan.
- Treating plan names or tiers as a substitute for checking the actual policy terms.

The system should use confirmed plan information and avoid unsupported assumptions.

## 4. Accountability

Chatbot outputs should be reviewed by the **project owner / responsible team** before the system is relied on for real member decisions.

The chatbot is an assistance tool, not a replacement for member support or qualified professionals. Uncertain or unsupported questions should be referred to member support rather than answered by guessing.

## 5. Data Fields in the Current Files

`plans.csv` contains these fields:

plan_id, plan_name, monthly_premium, annual_deductible, copay_pct, coverage_type, network_tier

`claims.csv` contains these fields:

claim_id, member_id, plan_id, procedure, claim_amount, status, date_filed
