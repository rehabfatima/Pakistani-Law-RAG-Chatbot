import chromadb

print("=" * 60)
print("CHROMADB INSPECTION")
print("=" * 60)

# Load existing database
client = chromadb.PersistentClient(path="chroma_db")

# Get collection
collection = client.get_collection(name="pakistani_law")

print("\nCollection name:")
print(collection.name)

print("\nTotal documents:")
print(collection.count())

# Get stored data
data = collection.get(
    include=["documents", "metadatas"]
)

print("\n" + "=" * 60)
print("STORED CHUNKS")
print("=" * 60)

for i, document in enumerate(data["documents"]):
    print(f"\n--- Chunk {i + 1} ---")
    print(document[:500])

print("\n" + "=" * 60)
print("DATABASE INSPECTION COMPLETED")
print("=" * 60)