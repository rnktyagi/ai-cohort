from langchain_text_splitters import RecursiveCharacterTextSplitter
import json
from datetime import datetime, timezone

benefits_text=""
claims_text=""
enrollment_text=""

with open("raw_text/benefits.txt", "r", encoding="utf-8") as f:
    benefits_text = f.read()

with open("raw_text/claims_process.txt", "r", encoding="utf-8") as f:  
    claims_text = f.read()

with open("raw_text/enrollment.txt", "r", encoding="utf-8") as f:
    enrollment_text = f.read()

splitter = RecursiveCharacterTextSplitter(chunk_size=500 , chunk_overlap=50)

benefits_text_chunks = splitter.split_text(benefits_text)
claims_text_chunks = splitter.split_text(claims_text)
enrollment_text_chunks = splitter.split_text(enrollment_text)

knowledge_base = []

ingested_at = datetime.now(timezone.utc).isoformat()

for i, chunk in enumerate(benefits_text_chunks, start=1):
    knowledge_base.append({
        "id": f"benefits_{i}",
        "text": chunk,
        "source_file": "benefits.txt",
        "source_type": "unstructured",
        "plan_type": "Gold PPO",
        "section": "coverage",
        "ingested_at": ingested_at
    })

for i, chunk in enumerate(claims_text_chunks, start=1):
    knowledge_base.append({
        "id": f"claims_{i}",
        "text": chunk,
        "source_file": "claims_process.txt",
        "source_type": "unstructured",
        "plan_type": "general",
        "section": "claims",
        "ingested_at": ingested_at
    })

for i, chunk in enumerate(enrollment_text_chunks, start=1):
    knowledge_base.append({
        "id": f"enrollment_{i}",
        "text": chunk,
        "source_file": "enrollment.txt",
        "source_type": "unstructured",
        "plan_type": "general",
        "section": "enrollment",
        "ingested_at": ingested_at
    })

with open("knowledge_base.jsonl", "w", encoding="utf-8") as f:
    for item in knowledge_base:
        f.write(json.dumps(item) + "\n")