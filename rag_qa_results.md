RAG QA Results — Day 10 Full Pipeline

Test setup

The same 10 Day 10 questions were run through the full pipeline:

question → retrieve() → SQL / Chroma / both → context → generate_answer()

Results

#

Question

Final answer

Assessment

1

What's my deductible?

I’m sorry, I don’t have that information. Please contact support.

Partial — well-formed and safe, but does not answer because no specific member/plan is identified.

2

What is the deductible for each plan?

Gold PPO: $2,000; Silver HMO: $1,500; Bronze HMO: $1,000.

Good — correct and well-formed.

3

What is the monthly premium?

I’m not sure which plan you’re referring to. Please contact support for the specific monthly premium.

Partial — safe, but the current SQL context contains all plan premiums rather than one member-specific premium.

4

What is the premium for each plan?

Gold PPO: $500; Silver HMO: $300; Bronze HMO: $150.

Good — correct and well-formed.

5

Is maternity care covered?

I’m not sure—maternity care isn’t listed in the sample summary. Please contact your plan’s support team for clarification.

Good — does not invent coverage.

6

Is physical therapy covered?

I’m not sure if physical therapy is covered under this plan. Please contact your insurance support team for clarification.

Good — does not invent coverage.

7

Is emergency care covered?

Yes. Emergency care is covered under the plan. In-network emergency room visits are subject to a 20% coinsurance after the deductible has been met.

Good — supported by the retrieved benefits summary.

8

What procedures are excluded from coverage?

I’m not sure—please contact support for details on excluded procedures.

Good — no unsupported exclusions are invented.

9

What benefits are covered by the plan?

The answer lists the Gold PPO benefits from the retrieved summary, including the $500 monthly premium, $2,000 deductible, primary-care and specialist coinsurance, emergency-room coinsurance, $15 generic prescription copay, and $6,500 out-of-pocket maximum.

Good — readable and grounded in retrieved context.

10

Is maternity care covered and what is the deductible?

I’m not sure—maternity care isn’t mentioned in the information provided. For details on coverage and the deductible, please contact your insurance support team.

Partial — correctly avoids claiming maternity coverage, but does not provide the deductible even though SQL retrieved deductible values.

Comparison against the Day 10 baseline

The Day 10 baseline showed that SQL retrieval returned structured values and Chroma retrieval returned policy chunks. The full RAG pipeline now converts those retrieved results into natural-language answers instead of exposing raw tuples or raw chunks.

Correctness and answer quality

The structured “each plan” questions are answered correctly. The unstructured questions are generally handled appropriately. The answers are well-formed sentences rather than raw retrieved chunks.

Questions 1 and 3 remain partial because the current schema/query does not identify which plan belongs to “me.” The mixed question (10) successfully uses both retrieval sources, but the generated answer prioritizes the missing maternity information and fails to state the available deductible values.

Coverage safety

Yes. The pipeline avoids overstating coverage that is not clearly confirmed. In particular, it does not claim that maternity care or physical therapy is covered when the retrieved context does not explicitly establish that.

Overall assessment

The full pipeline successfully performs:

retrieve → generate → grounded answer

The main remaining limitation is member-specific structured lookup: questions using “my” need a member-to-plan relationship in the SQL lookup. The mixed question also shows that the final generation prompt could be improved to ensure that every part of a multi-part question is answered when the context contains the required information.