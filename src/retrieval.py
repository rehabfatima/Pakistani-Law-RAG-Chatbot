import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHROMA_PATH = PROJECT_ROOT / "chroma_db"


# --------------------------------------------------
# Configuration
# --------------------------------------------------

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

COLLECTION_NAME = "pakistani_law"


# --------------------------------------------------
# Load embedding model
# --------------------------------------------------

print("=" * 60)
print("PAKISTANI LAW RAG - RETRIEVAL")
print("=" * 60)

print("\nLoading embedding model...")

model = SentenceTransformer(
    EMBEDDING_MODEL
)

print("Embedding model loaded!")


# --------------------------------------------------
# Connect to ChromaDB
# --------------------------------------------------

print("\nConnecting to ChromaDB...")

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_collection(
    name=COLLECTION_NAME
)

print("Connected successfully!")

print(
    "Total documents:",
    collection.count()
)


# --------------------------------------------------
# Retrieval function
# --------------------------------------------------

def retrieve(query, top_k=3):
    """
    Retrieve the most relevant legal chunks for a user query.

    The query is converted into the same embedding space
    as the stored legal chunks. ChromaDB then returns the
    closest chunks according to vector similarity.

    Args:
        query: User's legal question.
        top_k: Number of chunks to retrieve.

    Returns:
        List of dictionaries containing:
        - text
        - distance
        - section
        - chunk_id
        - source
    """

    if not query or not query.strip():
        return []

    # Convert query into embedding
    query_embedding = model.encode(
        [query]
    )[0]

    # Search vector database
    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=top_k
    )

    retrieved_chunks = []

    documents = results["documents"][0]

    distances = results["distances"][0]

    metadatas = results["metadatas"][0]

    for i in range(len(documents)):

        metadata = metadatas[i]

        retrieved_chunks.append(
            {
                "text": documents[i],
                "distance": distances[i],
                "section": metadata.get(
                    "section",
                    0
                ),
                "chunk_id": metadata.get(
                    "chunk_id",
                    i
                ),
                "source": metadata.get(
                    "source",
                    ""
                )
            }
        )

    return retrieved_chunks


# --------------------------------------------------
# Test retrieval
# --------------------------------------------------

if __name__ == "__main__":

    query = (
        "What is the minimum age for a child "
        "under this law?"
    )

    print("\n" + "=" * 60)
    print("QUERY")
    print("=" * 60)

    print(query)

    results = retrieve(
        query,
        top_k=5
    )

    print("\n" + "=" * 60)
    print("TOP 5 RETRIEVED CHUNKS")
    print("=" * 60)

    for i, result in enumerate(
        results,
        1
    ):

        print(
            f"\n--- RESULT {i} ---"
        )

        print(
            "Distance:",
            result["distance"]
        )

        print(
            "Section:",
            result["section"]
        )

        print(
            "Chunk ID:",
            result["chunk_id"]
        )

        print("\nText:")

        print(
            result["text"]
        )

        print("-" * 60)


    print("\n" + "=" * 60)
    print("RETRIEVAL COMPLETED")
    print("=" * 60)