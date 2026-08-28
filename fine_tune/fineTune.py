from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments

from peft import LoraConfig
from trl import SFTTrainer

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

dataset = load_dataset(
    "json",
    data_files="fine_tune_train.jsonl",
    split="train"
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=[
        "q_proj",
        "v_proj"
    ],
)

training_args = TrainingArguments(
    output_dir="./fine_tuned_model",
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    logging_steps=1,
    save_strategy="epoch",
    report_to="none",
)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    peft_config=lora_config,
)

trainer.train()

trainer.save_model("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")