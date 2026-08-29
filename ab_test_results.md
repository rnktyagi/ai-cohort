# A/B Test Results

## Test Setup

The same 15 insurance questions were evaluated using two prompt variants.

- **Variant A:** Basic context-based prompt.
- **Variant B:** Strict prompt requiring confirmed information, no unsupported assumptions, and explicit handling of missing information.

## Results

| # | Question | Variant A | Variant B |
|---|---|---|---|
| 1 | Is physical therapy covered under plan SILVER? | Good | Good |
| 2 | Is maternity care covered? | Good | Good |
| 3 | Is emergency care covered? | Good | Good |
| 4 | What is the deductible for plan GOLD? | Good | Good |
| 5 | What is the monthly premium? | Good | Good |
| 6 | Are preventive services covered? | Good | Good |
| 7 | What procedures are excluded from coverage? | Good | Good |
| 8 | Is dental surgery covered under plan SILVER? | Poor | Good |
| 9 | What benefits are covered by the plan? | Good | Good |
| 10 | What is the copay for primary care? | Good | Good |
| 11 | What is the status of claim CLM001? | Good | Good |
| 12 | What is the status of claim CLM002? | Good | Good |
| 13 | Has claim CLM003 been approved? | Poor | Good |
| 14 | Can I check the details of claim CLM001? | Good | Good |
| 15 | What happens if a claim is denied? | Good | Good |

## Scores

- **Variant A:** 13/15 good answers — **86.7%**
- **Variant B:** 15/15 good answers — **100%**

## Conclusion

Variant B performed better, with 2 additional good answers compared with Variant A.

The difference is noticeable but should not be treated as strong statistical evidence because the experiment contains only 15 questions. The result suggests that the stricter prompt may reduce unsupported assumptions, but a larger test set would be needed before considering the improvement meaningful.

**Winner: Variant B**
