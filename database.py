import chromadb
# pyrefly: ignore [missing-import]
import ollama

from splitter import split_text


# đọc file

with open(
    "data.txt",
    "r",
    encoding="utf-8"
) as f:
    text = f.read()


# chia chunk

chunks = split_text(
    text,
    chunk_size=20
)


# tạo embedding

embeddings = []

for chunk in chunks:

    result = ollama.embeddings(
        model="nomic-embed-text",
        prompt=chunk
    )

    embeddings.append(
        result["embedding"]
    )


# lưu ChromaDB

client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_or_create_collection(
    name="knowledge"
)


ids = [
    f"chunk_{i}"
    for i in range(len(chunks))
]


collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=ids
)


print("Đã tạo database")