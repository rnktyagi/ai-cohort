from openai import OpenAI
from dotenv import load_dotenv
from retrieval_engine import retrieve
import os

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"]
)

questions = [
    "Is physical therapy covered under plan SILVER?",
    "Is maternity care covered?",
    "Is emergency care covered?",
    "What is the deductible for plan GOLD?",
    "What is the monthly premium?",
    "Are preventive services covered?",
    "What procedures are excluded from coverage?",
    "Is dental surgery covered under plan SILVER?",
    "What benefits are covered by the plan?",
    "What is the copay for primary care?",
    "What is the status of claim CLM001?",
    "What is the status of claim CLM002?",
    "Has claim CLM003 been approved?",
    "Can I check the details of claim CLM001?",
    "What happens if a claim is denied?"
]

def generate_answer(question, context, variant):
    if variant == "A":
        prompt = f"""
Answer using the context below.

Context:
{context}

Question:
{question}
"""
    else:
        prompt = f"""
Answer using ONLY confirmed information from the context.
Do not guess or assume coverage.
If the answer is not available, clearly say that the information is unavailable.

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

with open("ab_test_results.md", "w", encoding="utf-8") as file:
    file.write("# A/B Test Results\n\n")
    file.write("| # | Question | Variant A | Variant B |\n")
    file.write("|---|---|---|---|\n")

    for i, question in enumerate(questions, 1):
        print(f"Running {i}/15")

        context = retrieve(question)

        answer_a = generate_answer(question, context, "A")
        answer_b = generate_answer(question, context, "B")

        answer_a = answer_a.replace("\n", " ")
        answer_b = answer_b.replace("\n", " ")

        file.write(
            f"| {i} | {question} | {answer_a} | {answer_b} |\n"
        )

print("A/B test completed.")
print("Results saved to ab_test_results.md")