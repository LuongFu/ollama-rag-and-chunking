import chromadb
# pyrefly: ignore [missing-import]
import ollama
import hashlib

from studies.splitter import split_text
from studies.postgres_loader import load_products

# =========================
# Persistent database
# =========================

client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_or_create_collection(
    name="knowledge"
)



# =========================
# đọc file
# =========================

# with open(
#     "data.txt",
#     "r",
#     encoding="utf-8"
# ) as f:

#     text = f.read()

documents, metadata = load_products()

# =========================
# chunk
# =========================

# chunks = split_text(
#     text,
#     chunk_size=20
# )



# =========================
# lấy dữ liệu đã có
# =========================

existing = collection.get()


existing_ids = set(
    existing["ids"]
)



# =========================
# chuẩn bị dữ liệu mới
# =========================

new_documents = []
new_embeddings = []
new_ids = []
new_metadata = []



# =========================
# thêm chunk mới
# =========================

# for index, chunk in enumerate(chunks):


#     chunk_id = hashlib.md5(
#         chunk.encode()
#     ).hexdigest()



#     # đã tồn tại thì bỏ qua

#     if chunk_id in existing_ids:
#         continue



#     print(
#         "Đang thêm:",
#         chunk[:50]
#     )



#     embedding = ollama.embeddings(
#         model="nomic-embed-text",
#         prompt=chunk
#     )



#     new_documents.append(
#         chunk
#     )


#     new_embeddings.append(
#         embedding["embedding"]
#     )


#     new_ids.append(
#         chunk_id
#     )


#     new_metadata.append(
#         {
#             "source": "data.txt",
#             "chunk_index": index,
#             "category": "knowledge"
#         }
#     )

for index, doc in enumerate(documents):

    embedding = ollama.embeddings(
        model="nomic-embed-text",
        prompt=doc
    )


    collection.add(
        documents=[doc],
        embeddings=[
            embedding["embedding"]
        ],
        ids=[
            f"product_{index}"
        ],
        metadatas=[
            metadata[index]
        ]
    )

# =========================
# lưu vào ChromaDB
# =========================

if new_ids:

    collection.add(
        documents=new_documents,
        embeddings=new_embeddings,
        ids=new_ids,
        metadatas=new_metadata
    )


    print(
        "Đã thêm",
        len(new_ids),
        "chunks mới"
    )


else:

    print(
        "Không có dữ liệu mới"
    )