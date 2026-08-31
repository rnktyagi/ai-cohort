from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"]
)


def generate_answer(question, context, chunk_ids=None):
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
        temperature=0,
        stream=True
    )

    answer = ""

    for chunk in response:
        token = chunk.choices[0].delta.content

        if token:
            answer += token
            yield token

    return chunk_ids