# pyrefly: ignore [missing-import]
import ollama
import chromadb

from splitter import split_text



# =====================
# đọc file
# =====================

with open(
    "data.txt",
    "r",
    encoding="utf-8"
) as f:
    text = f.read()



# =====================
# chunk
# =====================

chunks = split_text(
    text,
    chunk_size=20
)



# =====================
# tạo embedding
# =====================

embeddings = []


for chunk in chunks:

    result = ollama.embeddings(
        model="nomic-embed-text",
        prompt=chunk
    )

    embeddings.append(
        result["embedding"]
    )



# =====================
# ChromaDB
# =====================

client = chromadb.Client()


collection = client.create_collection(
    name="knowledge_embedding"
)



ids = []

for i in range(len(chunks)):
    ids.append(
        f"chunk_{i}"
    )



collection.add(

    documents=chunks,

    embeddings=embeddings,

    ids=ids
)



print("Đã lưu", len(chunks), "chunks")