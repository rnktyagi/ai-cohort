import json
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

INPUT_FILE = "ragas_eval_set.jsonl"
OUTPUT_FILE = "ragas_results.json"


def load_eval_set():
    rows = []

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))

    return rows


def run_rag_pipeline(question):
    # Replace this function with the project's retrieve() + generate_answer()
    # calls when running against the live RAG pipeline.
    context = (
        "Insurance policy context for the requested question. "
        "The evaluation harness records the retrieved context here."
    )

    answer = (
        "Answer generated from the retrieved insurance policy context."
    )

    return context, answer


def main():
    records = load_eval_set()
    rows = []

    for item in records:
        context, answer = run_rag_pipeline(item["question"])

        rows.append({
            "question": item["question"],
            "contexts": [context],
            "answer": answer,
            "ground_truth": item["ideal_answer"],
        })

    dataset = Dataset.from_list(rows)

    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ],
    )

    print(result)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result.to_pandas().to_dict(orient="records"), f, indent=2)

    print(f"Saved RAGAS results to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()