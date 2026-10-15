import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
import sys


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHROMA_PATH = PROJECT_ROOT / "chroma_db"

PDF_PATH = (
    PROJECT_ROOT
    / "data"
    / "The Islamabad Capital Territory Child Marriage Restraint Act, 2025 (Act No. XI of 2025) (1).pdf"
)


# --------------------------------------------------
# Import preprocessing functions
# --------------------------------------------------

sys.path.append(str(PROJECT_ROOT))

from src.preprocessing import (
    extract_text,
    clean_text,
    create_chunks
)


# --------------------------------------------------
# Configuration
# --------------------------------------------------

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

COLLECTION_NAME = "pakistani_law"


# --------------------------------------------------
# Main
# --------------------------------------------------

print("=" * 60)
print("PAKISTANI LAW RAG - EMBEDDINGS & VECTOR STORE")
print("=" * 60)


# --------------------------------------------------
# 1. Load embedding model
# --------------------------------------------------

print("\nLoading embedding model...")

model = SentenceTransformer(EMBEDDING_MODEL)

print("Embedding model loaded!")
print("Model:", EMBEDDING_MODEL)


# --------------------------------------------------
# 2. Read and preprocess PDF
# --------------------------------------------------

print("\nReading PDF...")

raw_text = extract_text(PDF_PATH)

cleaned_text = clean_text(raw_text)

chunks = create_chunks(cleaned_text)

print("Total chunks:", len(chunks))


# --------------------------------------------------
# 3. Prepare chunk texts
# --------------------------------------------------

chunk_texts = [
    chunk["text"]
    for chunk in chunks
]


# --------------------------------------------------
# 4. Create embeddings
# --------------------------------------------------

print("\nCreating embeddings...")

embeddings = model.encode(
    chunk_texts,
    show_progress_bar=True
)

print("Embeddings created!")

print(
    "Embedding shape:",
    embeddings.shape
)


# --------------------------------------------------
# 5. Create ChromaDB
# --------------------------------------------------

print("\nCreating ChromaDB...")

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)


# Delete old collection so that the improved
# preprocessing is stored from a clean state.

try:
    client.delete_collection(
        name=COLLECTION_NAME
    )

    print("Old collection removed.")

except Exception:
    print("No old collection found.")


collection = client.create_collection(
    name=COLLECTION_NAME
)

print("ChromaDB collection ready!")


# --------------------------------------------------
# 6. Store chunks + embeddings + metadata
# --------------------------------------------------

print("\nStoring chunks in ChromaDB...")

ids = [
    f"chunk_{i}"
    for i in range(len(chunks))
]

metadatas = []

for i, chunk in enumerate(chunks):

    metadata = {
        "source": PDF_PATH.name,
        "chunk_id": i,
        "section": chunk["section"]
    }

    if "part" in chunk:
        metadata["part"] = chunk["part"]

    metadatas.append(metadata)


collection.add(
    ids=ids,
    documents=chunk_texts,
    embeddings=embeddings.tolist(),
    metadatas=metadatas
)


print("Chunks stored successfully!")

print(
    "Vectors stored:",
    collection.count()
)


# --------------------------------------------------
# 7. Test retrieval
# --------------------------------------------------

query = (
    "What is the minimum age for a child under this law?"
)


print("\n" + "=" * 60)
print("TEST QUERY")
print("=" * 60)

print(query)


# Create query embedding
query_embedding = model.encode(
    [query]
)[0]


# Search ChromaDB
results = collection.query(
    query_embeddings=[
        query_embedding.tolist()
    ],
    n_results=5
)


# --------------------------------------------------
# 8. Print top results
# --------------------------------------------------

print("\n" + "=" * 60)
print("TOP 5 SIMILAR CHUNKS")
print("=" * 60)


for i in range(len(results["documents"][0])):

    document = results["documents"][0][i]

    distance = results["distances"][0][i]

    metadata = results["metadatas"][0][i]

    print(
        f"\n--- RESULT {i + 1} ---"
    )

    print(
        "Distance:",
        distance
    )

    print(
        "Section:",
        metadata["section"]
    )

    print("\nText:")
    print(document)

    print("-" * 60)


print("\n" + "=" * 60)
print("EMBEDDINGS & VECTOR STORE COMPLETED")
print("=" * 60)