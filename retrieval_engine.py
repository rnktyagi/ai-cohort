import sqlite3
import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = "coverage.db"

client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_collection("coverage_kb")
model = SentenceTransformer("all-MiniLM-L6-v2")

def question_classifier(question: str) :
    q = question.lower()

    structured_keywords = [
        "deductible",
        "claim status",
        "claim number",
        "claim amount",
        "how much have i paid",
        "remaining",
        "balance",
        "copay",
        "co-pay",
        "coinsurance",
        "premium",
        "member id",
        "plan id",
    ]

    unstructured_keywords = [
        "covered",
        "coverage",
        "procedure",
        "treatment",
        "exclusion",
        "excluded",
        "eligible",
        "benefit",
        "does my plan cover",
        "is this covered",
    ]

    has_structured = any(keyword in q for keyword in structured_keywords)
    has_unstructured = any(keyword in q for keyword in unstructured_keywords)

    if has_structured and has_unstructured:
        return "both"
    elif has_structured:
        return "structured"
    elif has_unstructured:
        return "unstructured"
    else:
        return "unstructured"

def sql_lookup(question):
    q = question.lower()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if "deductible" in q:
        sql = """
        SELECT plan_name, annual_deductible
        FROM plans;
        """

    elif "claim status" in q or "status of my claim" in q:
        sql = """
        SELECT claim_id, status
        FROM claims;
        """

    elif "claim amount" in q:
        sql = """
        SELECT claim_id, claim_amount
        FROM claims;
        """

    elif "premium" in q:
        sql = """
        SELECT plan_name, monthly_premium
        FROM plans;
        """

    else:
        conn.close()
        return "No SQL template available for this question."

    cursor.execute(sql)
    result = cursor.fetchall()

    conn.close()

    return result

def vector_lookup(question):
    query_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    return results["documents"][0]

def retrieve(question):
    classification = question_classifier(question)

    results = []

    if classification == "structured":
        results.extend(sql_lookup(question))

    elif classification == "unstructured":
        results.extend(vector_lookup(question))

    elif classification == "both":
        results.extend(sql_lookup(question))
        results.extend(vector_lookup(question))

    unique_results = []
    seen = set()

    for result in results:
        result = str(result).strip()

        if result and result not in seen:
            unique_results.append(result)
            seen.add(result)

    context = "\n\n".join(unique_results)

    return context