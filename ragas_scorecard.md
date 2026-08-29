# RAGAS Evaluation Scorecard

## Evaluation Set

- **Dataset:** `ragas_eval_set.jsonl`
- **Sample size:** 18 question / ideal-answer pairs
- **Domains:** deductibles, exclusions, claims status, plan details, plan comparison, coverage

## Metrics

| Metric | Purpose | Score |
|---|---|---:|
| Faithfulness | Measures whether the generated answer is supported by the retrieved context. | Pending live run |
| Answer Relevancy | Measures how directly the answer addresses the question. | Pending live run |
| Context Precision | Measures whether retrieved context is relevant to the question. | Pending live run |
| Context Recall | Measures whether the retrieved context contains information needed for the ideal answer. | Pending live run |

## Evaluation Pipeline

`ragas_eval_set.jsonl` → RAG pipeline → retrieved contexts + generated answers → RAGAS `evaluate()` → scorecard

## Conclusion

The evaluation set and RAGAS evaluation harness are prepared. Final metric values should be recorded only after running the harness against the live RAG pipeline; scores are intentionally not fabricated.
