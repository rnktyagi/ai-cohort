import json
import os
from ragas.llms import LangchainLLMWrapper
from dotenv import load_dotenv
from datasets import Dataset
from openai import OpenAI
from langchain_openai import ChatOpenAI
from retrieval_engine import retrieve
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

INPUT_FILE = "ragas_eval_set.jsonl"
OUTPUT_FILE = "ragas_results.json"

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"]
)


def load_eval_set():
    rows = []

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))

    return rows


def generate_answer(question, context):
    prompt = f"""
Answer using ONLY the context below.

If the answer isn't in the context, say you don't know
and suggest the member contact support.

This is not medical advice.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


def run_rag_pipeline(question):
    context = retrieve(question)

    answer = generate_answer(
        question,
        context
    )

    return context, answer


def main():
    records = load_eval_set()
    rows = []

    for item in records:
        context, answer = run_rag_pipeline(
            item["question"]
        )

        rows.append({
            "question": item["question"],
            "contexts": [context],
            "answer": answer,
            "ground_truth": item["ideal_answer"],
        })

    dataset = Dataset.from_list(rows)

    evaluator_llm = LangchainLLMWrapper(
    ChatOpenAI(
        model="openai/gpt-oss-20b",
        base_url="https://api.groq.com/openai/v1",
        api_key=os.environ["GROQ_API_KEY"],
        temperature=0,
    )
)
    evaluator_embeddings = LangchainEmbeddingsWrapper(
    HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
)

    result = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    ],
    llm=evaluator_llm,
    embeddings=evaluator_embeddings
)

    result_df = result.to_pandas()

    result_df.to_json(
        OUTPUT_FILE,
        orient="records",
        indent=2
    )

    print(result_df)
    print(f"\nSaved results to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()