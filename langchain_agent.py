from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from tools.tools import tools
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
    model="openai/gpt-oss-20b",
    temperature=0
)

system_prompt = """
You are a helpful assistant that replies in a warm, respectful, and formal tone.

Use the available tools when the user asks about coverage, claims, or plan details.
Never infer or assume coverage.
Use only confirmed information returned by the tools.
"""

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)


test_questions = [
    "Is physical therapy covered under plan SILVER?",
    "What is the status of claim CLM001?",
    "What are the details of plan GOLD?",
    "Can you check whether dental surgery is covered under plan SILVER?",
    "What is an insurance plan?"
]

for i, question in enumerate(test_questions, 1):
    print(f"\n{'=' * 60}")
    print(f"Test {i}")
    print(f"Question: {question}")

    response = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    })

    print("Answer:")
    print(response["messages"][-1].content)


