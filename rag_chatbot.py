from openai import OpenAI
import os
from dotenv import load_dotenv
from retrieval_engine import retrieve

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"]
)


def generate_answer(question, context):
    prompt = f"""
Answer using ONLY the context below.
If the answer isn't in the context, say you don't know and suggest the member contact support.
This is not medical advice.

Context: {context}

Question: {question}
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

def retrieve_and_answer(question):

    context = retrieve(question)
    answer = generate_answer(question, context)

    return answer

questions = [
    "What's my deductible?",
    "What is the deductible for each plan?",
    "What is the monthly premium?",
    "What is the premium for each plan?",
    "Is maternity care covered?",
    "Is physical therapy covered?",
    "Is emergency care covered?",
    "What procedures are excluded from coverage?",
    "What benefits are covered by the plan?",
    "Is maternity care covered and what is the deductible?",
]

for i, question in enumerate(questions, 1):
    print(f"\n{'=' * 60}")
    print(f"Question {i}: {question}")

    answer = retrieve_and_answer(question)

    print("Answer:")
    print(answer)