# Fine-Tuning Comparison

## Held-Out Test Results

| # | Question | Base model | Fine-tuned model |
|---|---|---|---|
| 1 | What is the Silver HMO deductible? | **Correct:** $1,500 | **Incorrect:** Said the deductible varies and gave an unsupported $10–$50 per month range. |
| 2 | What are the typical claim statuses? | **Correct:** Pending, Approved, and Denied. | **Incorrect:** Gave generic statuses such as Denied, Refunded, Paid, Partially Paid, and Fully Paid. |
| 3 | Does the context list specific maternity benefits? | **Correct:** Said the provided context did not list maternity benefits and suggested contacting support. | **Incorrect:** Claimed the context listed prenatal, hospital, and postpartum benefits, which were not provided. |
| 4 | What is the generic prescription copay? | **Partial:** Said the information was unavailable and suggested contacting support. | **Incorrect:** Gave an unsupported 5%–20% range instead of the $15 copay. |
| 5 | What is the annual out-of-pocket maximum? | **Correct:** $6,500. | **Incorrect:** Gave a generic explanation and examples instead of the $6,500 value. |

## Scores

| Metric | Base model | Fine-tuned model |
|---|---|---|
| Tone | Good | Partial |
| Correctness | Good | Poor |
| Disclaimer usage | Partial | Poor |
| Terminology clarity | Good | Partial |

## Conclusion

The fine-tuned model did **not meaningfully improve** the results. In fact, it performed worse on these 5 held-out questions and often invented information.

The base model was more reliable for this small test. Better prompting and retrieval/grounding would likely be more useful than more fine-tuning with this small dataset.
