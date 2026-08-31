# RAGAS Evaluation Scorecard

## Evaluation Summary

- **Test set:** 18 question / ideal-answer pairs
- **Evaluation framework:** RAGAS
- **Metrics:** faithfulness, answer relevancy, context precision, context recall
- **RAG pipeline:** Chroma retrieval + SQL lookup where applicable + Groq answer generation

## Results

The evaluation completed successfully and produced `ragas_results.json`.

The results contain valid metric values for some questions and `None` values for others. Therefore, the raw output should not be treated as a complete 18-question average for every metric.

| Metric | Observation |
|---|---|
| Faithfulness | Mixed. Some answers scored 0.0 while correctly grounded answers reached 1.0. |
| Answer relevancy | Mixed, ranging from 0.0 to 1.0 in the available results. |
| Context precision | Frequently missing (`None`), with some valid results near 0.0 and 1.0. |
| Context recall | Mixed. Available results include 0.0, 0.3333, and 1.0. |

## Weakest Metric

**Context precision is the main area to improve.**

The retrieved context frequently contains large amounts of irrelevant information. Silver-plan questions often retrieve the Gold PPO summary and generic claims/enrollment material instead of Silver-specific information.

## Key Failure Cases

### 1. Silver-plan retrieval

Questions about physical therapy, dental surgery, and exclusions for the SILVER plan returned primarily Gold-plan and generic content.

The generated answers therefore could not provide the ideal Silver-plan answers.

### 2. Claim-status retrieval

Questions about `CLM001` returned generic claims-process information instead of the actual claim record.

The ideal answer says that `CLM001` is approved, but the retrieved context did not contain that claim-specific record.

### 3. Plan comparison

The GOLD vs SILVER comparison retrieved Gold information but not enough Silver-specific evidence.

The model avoided inventing Silver details, but failed to provide the expected comparison.

### 4. Unavailable information

When the supplied context did not contain the answer, the model generally said it did not know and directed the member to support.

This is preferable to fabricating an answer.

## Re-run Recommendation

The next evaluation should focus on retrieval quality:

1. Add or verify Silver-plan documents/chunks in the knowledge base.
2. Ensure claim records such as `CLM001` are available to the structured SQL lookup.
3. Improve routing between structured claim/plan questions and vector retrieval.
4. Reduce irrelevant chunks returned for plan-specific questions.
5. Re-run the same 18-question evaluation after these retrieval changes.

The re-run should compare the new metric values against this baseline and determine whether context precision and context recall improve.

## Conclusion

The RAGAS evaluation is operational, but the results show that the primary weakness is **retrieval/context quality rather than the basic answer-generation mechanism**.

The strongest cases are those where the correct information was present in the retrieved context. Major failures occur when the retriever returns generic or wrong-plan information.

Because the sample contains only 18 questions and several missing metric values, the results should be treated as a **small diagnostic baseline**, not a statistically strong benchmark.