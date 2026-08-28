from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import json

BASE_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
ADAPTER = "./fine_tuned_model"

tokenizer = AutoTokenizer.from_pretrained(ADAPTER)

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL
)

model = PeftModel.from_pretrained(
    base_model,
    ADAPTER
)

def generate_answer(question):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful health-plan support assistant. "
                "Answer clearly and concisely. "
                "Do not guess or overstate coverage. "
                "If information is unavailable, say you don't know "
                "and suggest contacting member support. "
                "This is not medical advice."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.1
    )

    answer = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[1]:],
        skip_special_tokens=True
    )

    return answer

with open("fine_tune_test.jsonl", "r", encoding="utf-8") as f:
    test_data = [
        json.loads(line)
        for line in f
        if line.strip()
    ]

for i, item in enumerate(test_data, 1):

    question = next(
        message["content"]
        for message in item["messages"]
        if message["role"] == "user"
    )

    answer = generate_answer(question)

    print("\n" + "=" * 60)
    print(f"Question {i}: {question}")
    print("\nFine-tuned answer:")
    print(answer)