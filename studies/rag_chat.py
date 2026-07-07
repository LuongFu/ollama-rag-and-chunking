import chromadb
# pyrefly: ignore [missing-import]
import ollama


client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_collection(
    name="knowledge"
)


question = input(
    "Bạn hỏi: "
)


# ==========================
# tạo embedding cho câu hỏi
# ==========================

question_embedding = ollama.embeddings(
    model="nomic-embed-text",
    prompt=question
)


# ==========================
# tìm chunk gần nhất
# ==========================

result = collection.query(
    query_embeddings=[
        question_embedding["embedding"]
    ],

    n_results=2,

    include=[
        "documents",
        "metadatas"
    ]
)

documents = result["documents"][0]

metadata = result["metadatas"][0]


for doc, meta in zip(documents, metadata):

    print("================")

    print(
        "Nguồn:",
        meta.get("source", "N/A")
    )
    
    if "table" in meta:
        print("Bảng:", meta["table"])

    print(
        "ID/Chunk:",
        meta.get("id", meta.get("chunk_index", "N/A"))
    )
    
    if "ten_thuoc" in meta:
        print("Tên thuốc:", meta["ten_thuoc"])

    print(doc)

context = "\n".join(
    result["documents"][0]
)



# ==========================
# gửi cho LLM
# ==========================

prompt = f"""
Dựa vào thông tin:

{context}


Trả lời câu hỏi:

{question}
"""


response = ollama.chat(
    model="vicuna:7b-v1.5-q5_1",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)


print(
    response["message"]["content"]
)