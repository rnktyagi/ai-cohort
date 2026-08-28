Retrieval Test Results

#

Question

Classification

Retrieved context

Manual score

1

What's my deductible?

structured

SQL returned deductibles: Gold PPO — $2,000; Silver HMO — $1,500; Bronze HMO — $1,000.

good

2

What is the deductible for each plan?

structured

SQL returned the deductible for all three plans: $2,000, $1,500, and $1,000 respectively.

good

3

What is the monthly premium?

structured

SQL returned premiums: Gold PPO — $500; Silver HMO — $300; Bronze HMO — $150.

good

4

What is the premium for each plan?

structured

SQL returned the monthly premium for all three plans: $500, $300, and $150 respectively.

good

5

Is maternity care covered?

unstructured

Top policy chunks mainly contained the Gold PPO Summary of Benefits, enrollment information, and general claims guidance. They did not explicitly state whether maternity care is covered.

poor

6

Is physical therapy covered?

unstructured

Retrieved chunks contained general plan benefits, claims guidance, and enrollment information, but no explicit physical-therapy coverage information.

poor

7

Is emergency care covered?

unstructured

Retrieved the Gold PPO benefits summary, which explicitly lists emergency-room coverage as 20% coinsurance after the deductible.

good

8

What procedures are excluded from coverage?

unstructured

Retrieved claims guidance and the benefits summary, but no specific list of excluded procedures was present.

poor

9

What benefits are covered by the plan?

unstructured

Retrieved the Gold PPO benefits summary, including primary care, specialist visits, emergency room, generic prescriptions, deductible, and out-of-pocket maximum.

good

10

Is maternity care covered and what is the deductible?

both

SQL returned plan deductibles ($2,000 / $1,500 / $1,000), while vector retrieval returned the policy/benefits context. The retrieved policy text did not explicitly confirm maternity coverage.

partial

Summary

Good: 6/10

Partial: 1/10

Poor: 3/10

The structured SQL retrieval performed well for the questions supported by the plans schema. The weaker results came from unstructured questions where the current vector knowledge base does not contain explicit information about maternity care, physical therapy, or excluded procedures.