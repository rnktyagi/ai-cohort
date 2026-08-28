from sentence_transformers import SentenceTransformer
import chromadb

client = chromadb.PersistentClient(path="./chroma_data")

collection = client.get_collection("coverage_kb")

model=SentenceTransformer('all-MiniLM-L6-v2')

query = "Is physical therapy covered under the Silver plan?"

query_embedding = model.encode(query).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=1,
)

print(results)

filtered_results = collection.query(
    query_embeddings=[query_embedding],
    n_results=1,
    where={"plan_type": "Silver"},
)

print(filtered_results)