import os, ollama, chromadb

EMBED_MODEL = "nomic-embed-text"
KB_DIR = "knowledge"

client = chromadb.PersistentClient(path="./chroma_db")
try:
    client.delete_collection("acme_kb")   # start clean each run
except Exception:
    pass
col = client.create_collection("acme_kb")

def embed(text):
    return ollama.embeddings(model=EMBED_MODEL, prompt=text)["embedding"]

for i, fn in enumerate(sorted(f for f in os.listdir(KB_DIR) if f.endswith(".txt"))):
    text = open(os.path.join(KB_DIR, fn)).read()
    col.add(ids=[f"doc-{i}"], documents=[text],
            embeddings=[embed(text)], metadatas=[{"source": fn}])
    print(f"ingested {fn} ({len(text)} chars)")

print("done.")
