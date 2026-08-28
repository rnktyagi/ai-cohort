import json
import numpy as np
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

client = chromadb.PersistentClient(path="./chroma_data")

collection=client.create_collection("coverage_kb")

with open("knowledge_base.jsonl",'r') as f :
    kb=[json.loads(line) for line in f]

embeddings=np.load("embeddings.npy")

ids=[chunk['id'] for chunk in kb]
documents=[chunk['text'] for chunk in kb]

metadata=[{'source_file' : chunk['source_file'], 'source_type': chunk['source_type'] , 'section': chunk['section'] , 'plan_type': chunk['plan_type'] , 'ingested_at': chunk['ingested_at']} for chunk in kb]

collection.add(
    ids=ids,
    documents=documents,
    metadatas=metadata,
    embeddings=embeddings.tolist()
)