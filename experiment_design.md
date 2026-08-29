# A/B Experiment Design

## Objective

Compare two chatbot prompt variants to determine which produces better insurance answers.

## Variants

**Variant A — Current Prompt**

Uses the existing RAG prompt with conversation history and retrieved policy context.

**Variant B — Strict Prompt**

Uses the same retrieval and conversation history, but explicitly instructs the model to:
- Use only confirmed policy information.
- Avoid assumptions about coverage.
- Clearly state when information is unavailable.
- Give concise answers.

## Hypothesis

Variant B will produce a higher percentage of answers rated as good because the additional instructions should reduce unsupported assumptions and improve answer consistency.

## Metric

Each answer will be manually rated:

- **Good** — accurate, relevant, and clearly supported.
- **Poor** — incorrect, unsupported, or fails to answer the question.

The primary metric is:

**Good-answer rate = Good answers / 15 × 100**

## Sample Size

15 questions covering insurance coverage and claims scenarios.

The same 15 questions will be submitted to both variants.

## Procedure

1. Run all 15 questions through Variant A.
2. Run the same 15 questions through Variant B.
3. Record both answers.
4. Score each answer as Good or Poor.
5. Compare the good-answer rates.

## Decision Rule

The variant with the higher good-answer rate is the winner.

Because the sample contains only 15 questions, a small difference will not be considered strong evidence of a meaningful improvement.