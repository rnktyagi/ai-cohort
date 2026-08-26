from sentence_transformers import SentenceTransformer
import json
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

embedding = []

with open('knowledge_base.jsonl', 'r') as f:
    for line in f:
        data = json.loads(line)
        text = data['text']
        emb = model.encode(text)
        embedding.append(emb)

embedding=np.array(embedding)

np.save('embeddings.npy', embedding)